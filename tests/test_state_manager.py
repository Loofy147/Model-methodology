# tests/test_state_manager.py

import unittest
import os
import json
from jules_hf.core.state_manager import StateManager

class TestStateManager(unittest.TestCase):
    """
    Unit tests for the StateManager class.
    """

    def setUp(self):
        """
        Set up the test case.
        """
        self.state_file = "test_project_state.json"
        self.sm = StateManager(state_file_path=self.state_file)

    def tearDown(self):
        """
        Tear down the test case.
        """
        if os.path.exists(self.state_file):
            os.remove(self.state_file)

    def test_initial_state(self):
        """
        Test that the StateManager initializes with a default state if no state file exists.
        """
        self.assertEqual(self.sm.get_current_task(), None)
        self.assertEqual(self.sm.state["history"], [])

    def test_update_and_save_state(self):
        """
        Test that the StateManager can update and save the state correctly.
        """
        self.sm.update_state("TASK-1", "In Progress", "Doing the work")
        self.assertEqual(self.sm.get_current_task(), "TASK-1")

        # Verify that the state was saved to the file
        with open(self.state_file, "r") as f:
            saved_state = json.load(f)
        self.assertEqual(saved_state["current_task_id"], "TASK-1")

    def test_load_state(self):
        """
        Test that the StateManager can correctly load an existing state file.
        """
        # Create a dummy state file
        dummy_state = {"current_task_id": "TASK-2", "history": []}
        with open(self.state_file, "w") as f:
            json.dump(dummy_state, f)

        # Create a new StateManager to force it to load from the file
        sm2 = StateManager(state_file_path=self.state_file)
        self.assertEqual(sm2.get_current_task(), "TASK-2")

if __name__ == '__main__':
    unittest.main()
