"""
Unit tests for GeoMind Command-Line Interface (CLI).
"""
import subprocess
import sys
import unittest


class TestCLI(unittest.TestCase):

    def test_cli_version(self):
        result = subprocess.run(
            [sys.executable, "-m", "geomind", "--version"],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("GeoMind v", result.stdout)

    def test_cli_one_shot_distance(self):
        """Specifically verifies the prompt requirement: 'ditace between delhi & mumbi' via CLI."""
        result = subprocess.run(
            [sys.executable, "-m", "geomind", "ditace", "between", "delhi", "&", "mumbi"],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("Interpreted as: \"distance between Delhi and Mumbai\"", result.stdout)
        self.assertIn("1,148", result.stdout)
        self.assertIn("Mumbai", result.stdout)

    def test_cli_one_shot_history(self):
        result = subprocess.run(
            [sys.executable, "-m", "geomind", "causes", "and", "consequences", "of", "ww1"],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("World War I", result.stdout)
        self.assertIn("Causes", result.stdout)

    def test_cli_stdin_pipe(self):
        result = subprocess.run(
            [sys.executable, "-m", "geomind"],
            input="what is federalism\n",
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("Federalism", result.stdout)


    def test_cli_model_info(self):
        result = subprocess.run(
            [sys.executable, "-m", "geomind", "--model-info"],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("GeoMind-1", result.stdout)
        self.assertIn("Transformer", result.stdout)

    def test_cli_train_command(self):
        result = subprocess.run(
            [sys.executable, "-m", "geomind", "--train", "--epochs", "1"],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("Epoch 01/01", result.stdout)


if __name__ == "__main__":
    unittest.main()
