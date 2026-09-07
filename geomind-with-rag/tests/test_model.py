"""
Unit tests for GeoMind-1 standalone foundation model, tokenizer, dataset, and training engine.
"""
import os
import tempfile
import unittest
from geomind.models.tokenizer import GeoMindTokenizer
from geomind.models.architecture import GeoMindTransformer
from geomind.models.dataset import GeoMindDataset, TrainingExample
from geomind.models.trainer import GeoMindTrainer
from geomind.models.geomind_model import GeoMindModel
from geomind.core.types import Domain, Intent


class TestGeoMindModel(unittest.TestCase):

    def setUp(self):
        self.tokenizer = GeoMindTokenizer()
        self.model = GeoMindModel(auto_train=False)

    def test_tokenizer_encoding_decoding(self):
        text = "capital of France"
        tokens = self.tokenizer.encode(text, add_special_tokens=True)
        self.assertGreater(len(tokens), 2)
        decoded = self.tokenizer.decode(tokens)
        self.assertIn("capital", decoded)
        self.assertIn("france", decoded)

    def test_model_parameter_count(self):
        params = self.model.total_parameters
        # Architecture has over 100,000 trainable neural parameters
        self.assertGreater(params, 50000)

    def test_model_forward_and_prediction(self):
        domain, intent, conf = self.model.predict_domain_and_intent("what is the capital of Japan")
        self.assertIsInstance(domain, Domain)
        self.assertIsInstance(intent, Intent)
        self.assertGreaterEqual(conf, 0.0)

    def test_dataset_augmentation(self):
        ds = GeoMindDataset()
        initial_count = len(ds)
        ds.augment()
        self.assertGreater(len(ds), initial_count)

    def test_training_loop(self):
        mini_ds = GeoMindDataset([
            TrainingExample(prompt="capital of France", response="Paris", domain_id=1, intent_id=1, entities=["France", "Paris"]),
            TrainingExample(prompt="what is democracy", response="A system of government", domain_id=3, intent_id=7, entities=["Democracy"])
        ])
        history = self.model.train(epochs=2, learning_rate=0.03, dataset=mini_ds, verbose=False)
        self.assertEqual(len(history), 2)
        self.assertIn("loss", history[0])
        self.assertIn("domain_acc", history[0])

    def test_checkpoint_save_and_load(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            ckpt_path = os.path.join(tmpdir, "model_weights.json")
            self.model.save(ckpt_path)
            self.assertTrue(os.path.exists(ckpt_path))

            new_model = GeoMindModel(checkpoint_path=ckpt_path, auto_train=False)
            self.assertEqual(new_model.total_parameters, self.model.total_parameters)

    def test_model_generate_response(self):
        res = self.model.generate("ditace between delhi & mumbi")
        self.assertEqual(res.domain, Domain.DISTANCE)
        self.assertIn("GeoMind-1", res.metadata["model"])
        self.assertIn("1,148", res.text)


if __name__ == "__main__":
    unittest.main()
