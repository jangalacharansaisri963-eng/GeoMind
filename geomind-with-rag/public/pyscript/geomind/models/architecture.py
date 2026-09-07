"""
GeoMind Neural Model Architecture: Pure-Python Transformer & Neural Reasoner.
Implements Multi-Head Self-Attention, Feed-Forward Networks, Layer Normalization,
Domain/Intent Classification Heads, and Autoregressive Token Projection.
"""
import math
import operator
import random
from typing import Any, Dict, List, Optional, Tuple


# --- Fast Pure-Python Vector & Matrix Operations ---

def dot_product(v1: List[float], v2: List[float]) -> float:
    return sum(map(operator.mul, v1, v2))


def vec_add(v1: List[float], v2: List[float]) -> List[float]:
    return [x + y for x, y in zip(v1, v2)]


def vec_scale(v: List[float], s: float) -> List[float]:
    return [x * s for x in v]


def mat_vec_mul(matrix: List[List[float]], vector: List[float]) -> List[float]:
    """Computes matrix-vector product M * v."""
    return [dot_product(row, vector) for row in matrix]


def softmax(logits: List[float], temperature: float = 1.0) -> List[float]:
    """Applies numerically stable softmax."""
    if not logits:
        return []
    temp = max(1e-5, temperature)
    scaled = [x / temp for x in logits]
    max_val = max(scaled)
    exp_vals = [math.exp(x - max_val) for x in scaled]
    total = sum(exp_vals)
    return [x / total for x in exp_vals]


def gelu(x: float) -> float:
    """Gaussian Error Linear Unit approximation."""
    return 0.5 * x * (1.0 + math.tanh(math.sqrt(2.0 / math.pi) * (x + 0.044715 * (x ** 3))))


def layer_norm(
    vector: List[float],
    gamma: Optional[List[float]] = None,
    beta: Optional[List[float]] = None,
    eps: float = 1e-5
) -> List[float]:
    """Applies layer normalization with optional learned affine parameters."""
    n = len(vector)
    if n == 0:
        return []
    mean = sum(vector) / n
    variance = sum((x - mean) ** 2 for x in vector) / n
    std_inv = 1.0 / math.sqrt(variance + eps)

    normalized = [(x - mean) * std_inv for x in vector]
    if gamma is not None and beta is not None:
        return [g * x + b for g, x, b in zip(gamma, normalized, beta)]
    return normalized


def create_random_matrix(rows: int, cols: int, scale: float = 0.02) -> List[List[float]]:
    """Xavier/Glorot uniform initialization."""
    limit = math.sqrt(6.0 / (rows + cols)) * scale
    return [[random.uniform(-limit, limit) for _ in range(cols)] for _ in range(rows)]


def create_random_vector(dim: int, val: float = 0.0) -> List[float]:
    return [val for _ in range(dim)]


class MultiHeadAttention:
    """
    Multi-Head Attention block for contextual representation and query reasoning.
    """

    def __init__(self, hidden_dim: int, num_heads: int):
        assert hidden_dim % num_heads == 0, "hidden_dim must be divisible by num_heads"
        self.hidden_dim = hidden_dim
        self.num_heads = num_heads
        self.head_dim = hidden_dim // num_heads

        # Weight matrices: [out_dim x in_dim]
        self.w_q = create_random_matrix(hidden_dim, hidden_dim)
        self.w_k = create_random_matrix(hidden_dim, hidden_dim)
        self.w_v = create_random_matrix(hidden_dim, hidden_dim)
        self.w_o = create_random_matrix(hidden_dim, hidden_dim)

    def forward(self, seq: List[List[float]]) -> List[List[float]]:
        """
        Forward self-attention pass over sequence of hidden states.
        Input: list of vectors of length seq_len, each dimension hidden_dim.
        Output: list of vectors of length seq_len, each dimension hidden_dim.
        """
        seq_len = len(seq)
        if seq_len == 0:
            return []

        # Project queries, keys, values
        queries = [mat_vec_mul(self.w_q, x) for x in seq]
        keys = [mat_vec_mul(self.w_k, x) for x in seq]
        values = [mat_vec_mul(self.w_v, x) for x in seq]

        head_outputs: List[List[float]] = []

        # Multi-head attention loop
        scale = 1.0 / math.sqrt(self.head_dim)
        for i in range(seq_len):
            q_i = queries[i]
            # Attention scores for each head
            concatenated_heads: List[float] = []

            for h in range(self.num_heads):
                start = h * self.head_dim
                end = start + self.head_dim
                q_head = q_i[start:end]

                # Scaled dot-product scores against all keys in sequence
                scores: List[float] = []
                for j in range(seq_len):
                    k_head = keys[j][start:end]
                    score = dot_product(q_head, k_head) * scale
                    scores.append(score)

                # Attention weights
                attn_weights = softmax(scores)

                # Weighted sum over values
                head_context = [0.0] * self.head_dim
                for j in range(seq_len):
                    w = attn_weights[j]
                    v_head = values[j][start:end]
                    for d in range(self.head_dim):
                        head_context[d] += w * v_head[d]

                concatenated_heads.extend(head_context)

            # Final linear projection
            out_i = mat_vec_mul(self.w_o, concatenated_heads)
            head_outputs.append(out_i)

        return head_outputs


class FeedForwardNetwork:
    """Position-wise two-layer Feed-Forward Network with GELU activation."""

    def __init__(self, hidden_dim: int, intermediate_dim: int):
        self.w1 = create_random_matrix(intermediate_dim, hidden_dim)
        self.b1 = create_random_vector(intermediate_dim, 0.0)
        self.w2 = create_random_matrix(hidden_dim, intermediate_dim)
        self.b2 = create_random_vector(hidden_dim, 0.0)

    def forward(self, x: List[float]) -> List[float]:
        # Layer 1: intermediate = GELU(W1 * x + b1)
        h = mat_vec_mul(self.w1, x)
        h = [gelu(val + b) for val, b in zip(h, self.b1)]
        # Layer 2: out = W2 * intermediate + b2
        out = mat_vec_mul(self.w2, h)
        return [val + b for val, b in zip(out, self.b2)]


class TransformerBlock:
    """A standard Transformer encoder block with residual connections & LayerNorm."""

    def __init__(self, hidden_dim: int, num_heads: int, intermediate_dim: int):
        self.attention = MultiHeadAttention(hidden_dim, num_heads)
        self.ffn = FeedForwardNetwork(hidden_dim, intermediate_dim)
        self.ln1_gamma = [1.0] * hidden_dim
        self.ln1_beta = [0.0] * hidden_dim
        self.ln2_gamma = [1.0] * hidden_dim
        self.ln2_beta = [0.0] * hidden_dim

    def forward(self, seq: List[List[float]]) -> List[List[float]]:
        # Sub-layer 1: Self-attention with residual and layer norm
        attn_out = self.attention.forward(seq)
        norm1 = [
            layer_norm(vec_add(x, a), self.ln1_gamma, self.ln1_beta)
            for x, a in zip(seq, attn_out)
        ]

        # Sub-layer 2: Feed-forward with residual and layer norm
        ffn_out = [self.ffn.forward(x) for x in norm1]
        norm2 = [
            layer_norm(vec_add(x, f), self.ln2_gamma, self.ln2_beta)
            for x, f in zip(norm1, ffn_out)
        ]
        return norm2


class GeoMindTransformer:
    """
    GeoMind Foundation Model: A neural architecture optimized for Geography,
    History, and Social Studies reasoning.
    
    Includes learned token embeddings, sinusoidal positional encodings,
    multi-layer transformer blocks, and multi-task heads (intent/domain classifier
    and token probability generator).
    """

    def __init__(
        self,
        vocab_size: int,
        hidden_dim: int = 64,
        num_layers: int = 3,
        num_heads: int = 4,
        intermediate_dim: int = 128,
        num_domains: int = 5,
        num_intents: int = 10,
        max_seq_len: int = 128
    ):
        self.vocab_size = vocab_size
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.num_heads = num_heads
        self.intermediate_dim = intermediate_dim
        self.num_domains = num_domains
        self.num_intents = num_intents
        self.max_seq_len = max_seq_len

        # Token Embedding Table: [vocab_size x hidden_dim]
        self.token_embeddings = create_random_matrix(vocab_size, hidden_dim, scale=0.05)

        # Precomputed Positional Encodings: [max_seq_len x hidden_dim]
        self.pos_embeddings = self._build_positional_embeddings(max_seq_len, hidden_dim)

        # Transformer Layers
        self.blocks = [
            TransformerBlock(hidden_dim, num_heads, intermediate_dim)
            for _ in range(num_layers)
        ]

        # Final LayerNorm
        self.ln_f_gamma = [1.0] * hidden_dim
        self.ln_f_beta = [0.0] * hidden_dim

        # Multi-task heads
        # 1. Domain classification head: [num_domains x hidden_dim]
        self.domain_head = create_random_matrix(num_domains, hidden_dim)
        # 2. Intent classification head: [num_intents x hidden_dim]
        self.intent_head = create_random_matrix(num_intents, hidden_dim)
        # 3. LM Prediction Head: [vocab_size x hidden_dim]
        self.lm_head = create_random_matrix(vocab_size, hidden_dim, scale=0.03)

    def _build_positional_embeddings(self, max_len: int, dim: int) -> List[List[float]]:
        pe: List[List[float]] = []
        for pos in range(max_len):
            row: List[float] = []
            for i in range(dim):
                if i % 2 == 0:
                    val = math.sin(pos / (10000 ** (i / dim)))
                else:
                    val = math.cos(pos / (10000 ** ((i - 1) / dim)))
                row.append(val * 0.05)
            pe.append(row)
        return pe

    def count_parameters(self) -> int:
        """Calculates total trainable parameter count in the neural model."""
        total = 0
        # Token embeddings
        total += len(self.token_embeddings) * len(self.token_embeddings[0])
        # Positional embeddings
        total += len(self.pos_embeddings) * len(self.pos_embeddings[0])
        # Transformer blocks
        for b in self.blocks:
            # Attention W_q, W_k, W_v, W_o
            total += 4 * (self.hidden_dim * self.hidden_dim)
            # FFN W1, b1, W2, b2
            total += (self.intermediate_dim * self.hidden_dim) + self.intermediate_dim
            total += (self.hidden_dim * self.intermediate_dim) + self.hidden_dim
            # LayerNorms (ln1_gamma, ln1_beta, ln2_gamma, ln2_beta)
            total += 4 * self.hidden_dim
        # Final LayerNorm
        total += 2 * self.hidden_dim
        # Heads
        total += self.num_domains * self.hidden_dim
        total += self.num_intents * self.hidden_dim
        total += self.vocab_size * self.hidden_dim
        return total

    def forward(
        self,
        token_ids: List[int]
    ) -> Tuple[List[List[float]], List[float], List[float]]:
        """
        Forward pass through the transformer.
        Returns:
            - hidden_states: List of contextual vectors [seq_len x hidden_dim]
            - domain_logits: Prediction logits for domain classification
            - intent_logits: Prediction logits for intent classification
        """
        seq_len = min(len(token_ids), self.max_seq_len)
        if seq_len == 0:
            return ([], [0.0] * self.num_domains, [0.0] * self.num_intents)

        # 1. Look up token embeddings + add sinusoidal positional encodings
        hidden: List[List[float]] = []
        for pos in range(seq_len):
            tid = token_ids[pos]
            safe_tid = tid if 0 <= tid < self.vocab_size else 1  # 1 is <unk>
            t_emb = self.token_embeddings[safe_tid]
            p_emb = self.pos_embeddings[pos]
            hidden.append(vec_add(t_emb, p_emb))

        # 2. Pass through transformer layers
        for block in self.blocks:
            hidden = block.forward(hidden)

        # 3. Final layer norm
        hidden = [
            layer_norm(h, self.ln_f_gamma, self.ln_f_beta)
            for h in hidden
        ]

        # 4. Sequence pooled representation (mean pooling over non-padding tokens)
        pooled = [0.0] * self.hidden_dim
        for h in hidden:
            for d in range(self.hidden_dim):
                pooled[d] += h[d]
        pooled = [val / seq_len for val in pooled]

        # 5. Head projections
        domain_logits = mat_vec_mul(self.domain_head, pooled)
        intent_logits = mat_vec_mul(self.intent_head, pooled)

        return hidden, domain_logits, intent_logits

    def predict_next_token_logits(self, last_hidden_state: List[float]) -> List[float]:
        """Projects the last hidden state into vocabulary logits for next-token prediction."""
        return mat_vec_mul(self.lm_head, last_hidden_state)

    def export_state_dict(self) -> Dict[str, Any]:
        """Serializes weights into a portable dictionary for checkpointing."""
        return {
            "config": {
                "vocab_size": self.vocab_size,
                "hidden_dim": self.hidden_dim,
                "num_layers": self.num_layers,
                "num_heads": self.num_heads,
                "intermediate_dim": self.intermediate_dim,
                "num_domains": self.num_domains,
                "num_intents": self.num_intents,
                "max_seq_len": self.max_seq_len
            },
            "token_embeddings": self.token_embeddings,
            "domain_head": self.domain_head,
            "intent_head": self.intent_head,
            "lm_head": self.lm_head
        }

    def load_state_dict(self, state_dict: Dict[str, Any]) -> None:
        """Loads weights from a serialized checkpoint dictionary."""
        if "token_embeddings" in state_dict:
            self.token_embeddings = state_dict["token_embeddings"]
        if "domain_head" in state_dict:
            self.domain_head = state_dict["domain_head"]
        if "intent_head" in state_dict:
            self.intent_head = state_dict["intent_head"]
        if "lm_head" in state_dict:
            self.lm_head = state_dict["lm_head"]
