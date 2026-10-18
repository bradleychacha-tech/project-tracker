import subprocess
import sys
import unittest


class TestCLI(unittest.TestCase):
    def test_help(self):
        result = subprocess.run(
            [sys.executable, "main.py", "--help"],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("Project Tracker CLI", result.stdout)


if __name__ == "__main__":
    unittest.main()

# Tests