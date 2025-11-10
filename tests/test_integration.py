# tests/test_integration.py

import unittest
import os
from unittest.mock import patch, MagicMock
from jules_hf.main import main

class TestIntegration(unittest.TestCase):
    """
    Integration tests for the main application workflow.
    """

    def setUp(self):
        """
        Set up the test case.
        """
        self.state_file = "project_state.json"
        # Clean up state file before each test
        if os.path.exists(self.state_file):
            os.remove(self.state_file)

    def tearDown(self):
        """
        Tear down the test case.
        """
        if os.path.exists(self.state_file):
            os.remove(self.state_file)

    @patch('jules_hf.main.HuggingFaceClient')
    def test_end_to_end_workflow(self, MockHuggingFaceClient):
        """
        Test the full end-to-end workflow of the agent.
        """
        # I'll temporarily redirect stdout to capture the output of main()
        import sys
        from io import StringIO

        # Mock the HuggingFaceClient to avoid real API calls
        mock_hf_client_instance = MockHuggingFaceClient.return_value
        mock_hf_client_instance.run.side_effect = [
            "Successfully logged in to the Hugging Face Hub.",
            "Successfully created repository: https://huggingface.co/test-user/jules-test-repo-123"
        ]

        original_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        main()

        sys.stdout = original_stdout

        # Verify the output
        output = captured_output.getvalue()
        self.assertIn("--- Logging in to Hugging Face ---", output)
        self.assertIn("Login Result: Successfully logged in to the Hugging Face Hub.", output)
        self.assertIn("--- Creating a new repository on the Hub ---", output)
        self.assertIn("Create Repo Result: Successfully created repository: https://huggingface.co/test-user/jules-test-repo-123", output)

        # Verify that the state was saved
        self.assertTrue(os.path.exists(self.state_file))

if __name__ == '__main__':
    unittest.main()
