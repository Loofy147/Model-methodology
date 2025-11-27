# tests/test_methodology_engine.py

import unittest
import os
import shutil
import json
from jules_hf.core.methodology_engine import MethodologyEngine

class TestMethodologyEngine(unittest.TestCase):
    """
    Unit tests for the MethodologyEngine class.
    """

    def setUp(self):
        """
        Set up the test case with a temporary directory for user data.
        """
        self.test_user_dir = "test_jules_hf"
        self.test_plan_filename = "test_plan.json"

        # Clean up any old test directories
        if os.path.exists(self.test_user_dir):
            shutil.rmtree(self.test_user_dir)
        os.makedirs(self.test_user_dir)

    def tearDown(self):
        """
        Clean up the temporary test directory.
        """
        shutil.rmtree(self.test_user_dir)

    def test_plan_copy_on_first_load(self):
        """
        Test that the default plan is copied to the user directory on first load.
        """
        # Initialize the engine, which should trigger the copy
        engine = MethodologyEngine(user_dir=self.test_user_dir, plan_filename="plan.json")

        # Check that the plan file now exists in the user directory
        self.assertTrue(os.path.exists(engine.plan_file_path))

        # Check that the content is not empty and is valid JSON
        with open(engine.plan_file_path, 'r') as f:
            data = json.load(f)
        self.assertIn("project_name", data)

    def test_get_current_task(self):
        """
        Test that the MethodologyEngine can correctly identify the current task from a custom plan.
        """
        # Create a custom test plan file
        custom_plan_path = os.path.join(self.test_user_dir, self.test_plan_filename)
        custom_plan_data = {
            "project_name": "Test Project",
            "epics": [{"id": "E1", "status": "In Progress", "milestones": [
                {"id": "M1", "status": "In Progress", "features": [
                    {"id": "F1", "tasks": [{"id": "T1", "status": "Ready", "title": "Current"}]}
                ]}]
            }]
        }
        with open(custom_plan_path, 'w') as f:
            json.dump(custom_plan_data, f)

        engine = MethodologyEngine(user_dir=self.test_user_dir, plan_filename=self.test_plan_filename)
        current_task_info = engine.get_current_task()
        self.assertEqual(current_task_info["task"]["id"], "T1")

    def test_update_task_status(self):
        """
        Test that the MethodologyEngine can update a task's status and save the plan.
        """
        # Initialize the engine, which will copy the default plan
        engine = MethodologyEngine(user_dir=self.test_user_dir, plan_filename="plan.json")

        # Get the ID of the first ready task
        initial_task_info = engine.get_current_task()
        task_id_to_update = initial_task_info["task"]["id"]

        # Update the status
        result = engine.update_task_status(task_id_to_update, "Completed")
        self.assertTrue(result)

        # Verify the change by loading the plan again with a new engine instance
        new_engine = MethodologyEngine(user_dir=self.test_user_dir, plan_filename="plan.json")
        task_found = False
        for epic in new_engine.plan.get("epics", []):
            for milestone in epic.get("milestones", []):
                for feature in milestone.get("features", []):
                    for task in feature.get("tasks", []):
                        if task.get("id") == task_id_to_update:
                            self.assertEqual(task["status"], "Completed")
                            task_found = True
                            break
        self.assertTrue(task_found, f"Task '{task_id_to_update}' was not found after update.")


if __name__ == '__main__':
    unittest.main()
