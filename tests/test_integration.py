# tests/test_integration.py

import unittest
import os
import json
from jules_hf.main import main
from jules_hf.core.config import config

class TestIntegration(unittest.TestCase):
    """
    Integration tests for the main application workflow.
    """

    def setUp(self):
        """
        Set up the test case by ensuring a clean log file.
        """
        self.log_file = config.get('logging', {}).get('file', 'jules_hf.log')
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    def test_app_run_logs_correctly(self):
        """
        Test that the application runs and logs the correct information.
        """
        main()

        self.assertTrue(os.path.exists(self.log_file))

        with open(self.log_file, 'r') as f:
            log_lines = f.readlines()

        # Check for key log messages
        log_contents = "".join(log_lines)
        self.assertIn("Application starting...", log_contents)
        self.assertIn("Initializing JulesHF application...", log_contents)
        self.assertIn("Current task retrieved.", log_contents)
        self.assertIn("Application finished.", log_contents)

        # Check for structured log data
        found_task_log = False
        for line in log_lines:
            if not line:
                continue
            try:
                log_json = json.loads(line)
                if log_json.get("message") == "Current task retrieved.":
                    self.assertEqual(log_json.get("task_title"), "Implement the Methodology Engine")
                    found_task_log = True
                    break
            except json.JSONDecodeError:
                self.fail(f"Log line is not valid JSON: {line}")

        self.assertTrue(found_task_log, "Did not find the structured log for the current task.")


if __name__ == '__main__':
    unittest.main()
