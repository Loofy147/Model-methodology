# tests/test_integration.py

import unittest
import os
from jules_hf.main import main

class TestIntegration(unittest.TestCase):
    """
    Integration tests for the main application workflow.
    """

    def test_app_run(self):
        """
        Test that the application runs and correctly identifies the current task.
        """
        import sys
        from io import StringIO

        original_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        main()

        sys.stdout = original_stdout

        output = captured_output.getvalue()
        self.assertIn("Jules for Hugging Face - Running...", output)
        self.assertIn("Task Title: Implement the Methodology Engine", output)

if __name__ == '__main__':
    unittest.main()
