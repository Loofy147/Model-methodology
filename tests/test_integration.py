# tests/test_integration.py

import unittest
import os
import json
from unittest.mock import patch
from jules_hf.main import main
from jules_hf.core.config import config

class TestIntegration(unittest.TestCase):
    """
    Integration tests for the main application workflow.
    """

    @patch.dict('os.environ', {'HUGGING_FACE_HUB_TOKEN': 'test_token'})
    @patch('jules_hf.main.HuggingFaceLLMProvider') # Mock the real LLM provider
    def setUp(self, MockLLMProvider):
        """
        Set up the test case by ensuring a clean log file and mocking necessary components.
        """
        # We don't need the mock instance here, but it's passed by the decorator
        self.log_file = config.get('logging', {}).get('file', 'jules_hf.log')
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    @patch.dict('os.environ', {'HUGGING_FACE_HUB_TOKEN': 'test_token'})
    @patch('jules_hf.main.HuggingFaceLLMProvider') # Mock the real LLM provider
    def test_app_run_logs_correctly(self, MockLLMProvider):
        """
        Test that the application runs and logs the correct information.
        """
        # We don't need the mock instance here, but it's passed by the decorator
        main()

        self.assertTrue(os.path.exists(self.log_file))

        with open(self.log_file, 'r') as f:
            log_lines = f.readlines()

        log_contents = "".join(log_lines)
        self.assertIn("Application starting...", log_contents)
        self.assertIn("Initializing JulesHF application...", log_contents)
        self.assertIn("Current task retrieved.", log_contents)
        self.assertIn("Application finished.", log_contents)

        found_task_log = False
        for line in log_lines:
            if not line:
                continue
            try:
                log_json = json.loads(line)
                if log_json.get("message") == "Current task retrieved.":
                    self.assertEqual(log_json["extra_context"]["task_title"], "Implement the Methodology Engine")
                    found_task_log = True
                    break
            except (json.JSONDecodeError, KeyError):
                # Ignore lines that aren't valid JSON or don't have the expected structure
                continue

        self.assertTrue(found_task_log, "Did not find the structured log for the current task.")


if __name__ == '__main__':
    unittest.main()
