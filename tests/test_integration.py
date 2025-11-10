# tests/test_integration.py

import unittest
import os
from jules_hf.main import main

class TestIntegration(unittest.TestCase):
    """
    Integration tests for the main application workflow.
    """

    def setUp(self):
        """
        Set up the test case.
        """
        self.test_file = "new_file.txt"
        self.state_file = "project_state.json"

    def tearDown(self):
        """
        Tear down the test case.
        """
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists(self.state_file):
            os.remove(self.state_file)

    def test_end_to_end_workflow(self):
        """
        Test the full end-to-end workflow of the agent.
        """
        # I'll temporarily redirect stdout to capture the output of main()
        import sys
        from io import StringIO

        original_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        main()

        sys.stdout = original_stdout

        # Verify the output
        output = captured_output.getvalue()
        self.assertIn("Jules for Hugging Face - Initializing...", output)
        self.assertIn("Next Action: execute_tool('file_system_manager.create_file', {'file_path': 'new_file.txt'})", output)
        self.assertIn("Tool Execution Result: Successfully created file: new_file.txt", output)

        # Verify that the file was created
        self.assertTrue(os.path.exists(self.test_file))

        # Verify that the state was saved
        self.assertTrue(os.path.exists(self.state_file))

if __name__ == '__main__':
    unittest.main()
