# tests/test_methodology_engine.py

import unittest
import os
import shutil
import json
from unittest.mock import patch
from jules_hf.core.methodology_engine import MethodologyEngine
from jules_hf.core.config import Config

class TestMethodologyEngine(unittest.TestCase):
    """
    Unit tests for the MethodologyEngine class.
    """

    def setUp(self):
        """
        Set up the test case with a temporary directory and a mocked config.
        """
        self.test_user_dir = "test_jules_hf"
        self.test_plan_filename = "test_plan.json"

        # Mock the config to use our temporary test directory
        self.config_patch = patch.object(Config, 'get')
        self.mock_config_get = self.config_patch.start()

        def mock_get(key, default=None):
            if key == "user_data_dir":
                return self.test_user_dir
            if key == "plan_filename":
                return self.test_plan_filename
            return default

        self.mock_config_get.side_effect = mock_get

        # Clean up any old test directories
        if os.path.exists(self.test_user_dir):
            shutil.rmtree(self.test_user_dir)
        os.makedirs(self.test_user_dir)

    def tearDown(self):
        """
        Clean up the temporary test directory and stop the patcher.
        """
        self.config_patch.stop()
        shutil.rmtree(self.test_user_dir)

    def test_plan_copy_on_first_load(self):
        """
        Test that the default plan is copied to the user directory on first load.
        """
        self.mock_config_get.side_effect = lambda key, default=None: {
            "user_data_dir": self.test_user_dir,
            "plan_filename": "plan.json"
        }.get(key, default)

        engine = MethodologyEngine()
        self.assertTrue(os.path.exists(engine.plan_file_path))
        with open(engine.plan_file_path, 'r') as f:
            data = json.load(f)
        self.assertIn("project_name", data)

    def test_get_current_task(self):
        """
        Test that the MethodologyEngine can correctly identify the current task from a custom plan.
        """
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

        engine = MethodologyEngine()
        current_task_info = engine.get_current_task()
        self.assertEqual(current_task_info["task"]["id"], "T1")

    def test_update_task_status(self):
        """
        Test that the MethodologyEngine can update a task's status and save the plan.
        """
        self.mock_config_get.side_effect = lambda key, default=None: {
            "user_data_dir": self.test_user_dir,
            "plan_filename": "plan.json"
        }.get(key, default)

        engine = MethodologyEngine()
        initial_task_info = engine.get_current_task()
        task_id_to_update = initial_task_info["task"]["id"]

        result = engine.update_task_status(task_id_to_update, "Completed")
        self.assertTrue(result)

        new_engine = MethodologyEngine()
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
