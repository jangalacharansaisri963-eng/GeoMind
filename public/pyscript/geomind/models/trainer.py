"""
GeoMind Trainer: Training engine for GeoMind foundation models.
Supports parameter optimization, multi-task loss computation, learning rate scheduling,
and model checkpoint persistence.
"""
import math
import json
import random
from typing import Any, Callable, Dict, List, Optional, Tuple
from geomind.models.tokenizer import GeoMindTokenizer
from geomind.models.architecture import GeoMindTransformer, softmax, dot_product
from geomind.models.dataset import GeoMindDataset, TrainingExample


def cross_entropy_loss(logits: List[float], target_idx: int) -> float:
    """Calculates categorical cross-entropy loss."""
    probs = softmax(logits)
    target_prob = max(1e-12, probs[target_idx] if 0 <= target_idx < len(probs) else 1e-12)
    return -math.log(target_prob)


class GeoMindTrainer:
    """
    Supervised learning and fine-tuning engine for GeoMind neural architectures.
    """

    def __init__(
        self,
        model: GeoMindTransformer,
        tokenizer: GeoMindTokenizer,
        dataset: Optional[GeoMindDataset] = None,
        learning_rate: float = 0.02
    ):
        self.model = model
        self.tokenizer = tokenizer
        self.dataset = dataset or GeoMindDataset()
        self.learning_rate = learning_rate
        self.training_history: List[Dict[str, float]] = []

    def train_step(self, example: TrainingExample, lr: float) -> Tuple[float, float, bool, bool]:
        """
        Executes a single forward-backward parameter update step.
        Returns (domain_loss, intent_loss, is_domain_correct, is_intent_correct).
        """
        # Encode prompt tokens
        prompt_tokens = self.tokenizer.encode(example.prompt, add_special_tokens=True)
        if not prompt_tokens:
            return 0.0, 0.0, False, False

        # Forward pass
        hidden, domain_logits, intent_logits = self.model.forward(prompt_tokens)

        # Compute losses
        d_loss = cross_entropy_loss(domain_logits, example.domain_id)
        i_loss = cross_entropy_loss(intent_logits, example.intent_id)

        # Check accuracy before parameter update
        pred_d = domain_logits.index(max(domain_logits)) if domain_logits else -1
        pred_i = intent_logits.index(max(intent_logits)) if intent_logits else -1
        d_correct = (pred_d == example.domain_id)
        i_correct = (pred_i == example.intent_id)

        # Gradient update on classification heads
        # Domain head gradient
        d_probs = softmax(domain_logits)
        d_grad = list(d_probs)
        if 0 <= example.domain_id < len(d_grad):
            d_grad[example.domain_id] -= 1.0

        # Mean pooled vector
        seq_len = len(hidden)
        pooled = [0.0] * self.model.hidden_dim
        for h in hidden:
            for dim in range(self.model.hidden_dim):
                pooled[dim] += h[dim]
        pooled = [val / max(1, seq_len) for val in pooled]

        # Update domain head weights
        for d_idx in range(len(self.model.domain_head)):
            g = d_grad[d_idx]
            for dim in range(self.model.hidden_dim):
                self.model.domain_head[d_idx][dim] -= lr * g * pooled[dim]

        # Intent head gradient
        i_probs = softmax(intent_logits)
        i_grad = list(i_probs)
        if 0 <= example.intent_id < len(i_grad):
            i_grad[example.intent_id] -= 1.0

        # Update intent head weights
        for i_idx in range(len(self.model.intent_head)):
            g = i_grad[i_idx]
            for dim in range(self.model.hidden_dim):
                self.model.intent_head[i_idx][dim] -= lr * g * pooled[dim]

        # Update token embeddings slightly towards pooled representation
        for tid in prompt_tokens:
            if 0 <= tid < self.model.vocab_size:
                for dim in range(self.model.hidden_dim):
                    self.model.token_embeddings[tid][dim] += lr * 0.005 * pooled[dim]

        return d_loss, i_loss, d_correct, i_correct

    def train(
        self,
        epochs: int = 5,
        learning_rate: Optional[float] = None,
        progress_callback: Optional[Callable[[int, int, float], None]] = None,
        verbose: bool = True
    ) -> List[Dict[str, float]]:
        """
        Runs complete multi-epoch training loop across dataset examples.
        """
        lr = learning_rate or self.learning_rate
        total_examples = len(self.dataset)
        session_history: List[Dict[str, float]] = []

        for epoch in range(1, epochs + 1):
            epoch_loss = 0.0
            correct_domain = 0
            correct_intent = 0

            # Shuffle examples each epoch
            indices = list(range(total_examples))
            random.shuffle(indices)

            for idx in indices:
                ex = self.dataset[idx]
                d_loss, i_loss, d_correct, i_correct = self.train_step(ex, lr)
                epoch_loss += (d_loss + i_loss)
                if d_correct:
                    correct_domain += 1
                if i_correct:
                    correct_intent += 1

            avg_loss = epoch_loss / max(1, total_examples)
            domain_acc = (correct_domain / max(1, total_examples)) * 100
            intent_acc = (correct_intent / max(1, total_examples)) * 100

            epoch_record = {
                "epoch": epoch,
                "loss": round(avg_loss, 4),
                "domain_acc": round(domain_acc, 2),
                "intent_acc": round(intent_acc, 2)
            }
            self.training_history.append(epoch_record)
            session_history.append(epoch_record)

            if verbose:
                print(
                    f"Epoch {epoch:02d}/{epochs:02d} | "
                    f"Loss: {avg_loss:.4f} | "
                    f"Domain Acc: {domain_acc:.1f}% | "
                    f"Intent Acc: {intent_acc:.1f}%"
                )

            if progress_callback:
                progress_callback(epoch, epochs, avg_loss)

            # Decay learning rate
            lr *= 0.92

        return session_history

    def save_checkpoint(self, filepath: str) -> None:
        """Saves model weights and training metadata to disk."""
        data = {
            "model_state": self.model.export_state_dict(),
            "training_history": self.training_history,
            "total_parameters": self.model.count_parameters()
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load_checkpoint(self, filepath: str) -> None:
        """Loads model weights and history from a disk checkpoint."""
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        if "model_state" in data:
            self.model.load_state_dict(data["model_state"])
        if "training_history" in data:
            self.training_history = data["training_history"]
