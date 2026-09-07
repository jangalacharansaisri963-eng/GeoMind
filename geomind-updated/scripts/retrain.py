"""
CI training script for GeoMind-1.

Retrains the transformer backbone on the bundled dataset
(geomind/models/dataset.py) and overwrites the checkpoint committed at
geomind/data/geomind_weights.json. Runs on a normal Ubuntu GitHub Actions
runner — no Playwright/browser needed for this part, only for
scripts/research_check.py.

Usage:
    python scripts/retrain.py --epochs 10 --lr 0.02
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from geomind.models.geomind_model import GeoMindModel  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Retrain GeoMind-1 and save its checkpoint.")
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--lr", type=float, default=0.02)
    args = parser.parse_args()

    # auto_train=False: we're about to train explicitly below regardless of
    # whether a checkpoint already exists.
    model = GeoMindModel(auto_train=False)
    history = model.train(epochs=args.epochs, learning_rate=args.lr, verbose=True)

    weights_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "geomind", "data", "geomind_weights.json"
    )
    model.save(weights_path)
    print(f"Saved checkpoint to {weights_path} after {len(history)} epoch(s).")


if __name__ == "__main__":
    main()
