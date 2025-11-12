# tests/test_methodology_engine.py

import unittest
from jules_hf.core.methodology_engine import MethodologyEngine
from importlib import resources
import json

class TestMethodologyEngine(unittest.TestCase):
    """
    Unit tests for the MethodologyEngine class.
    """

    def setUp(self):
        """
        Set up the test case.
        """
        # Load the test plan using importlib.resources
        with resources.files('jules_hf').joinpath('test_plan.json').open('r') as f:
            test_plan_data = json.load(f)

        self.engine = MethodologyEngine() # it loads the default plan
        self.engine.plan = test_plan_data # we overwrite with the test plan

    def test_load_plan_success(self):
        """
        Test that the MethodologyEngine can successfully load a plan file.
        """
        self.assertNotIn("error", self.engine.plan)
        self.assertEqual(self.engine.plan["project_name"], "Test Project")

    def test_get_current_task(self):
        """
        Test that the MethodologyEngine can correctly identify the current task.
        """
        current_task_info = self.engine.get_current_task()
        self.assertEqual(current_task_info["epic"], "Test-Epic-2")
        self.assertEqual(current_task_info["milestone"], "Test-Milestone-1")
        self.assertEqual(current_task_info["task"]["id"], "T-2")
        self.assertEqual(current_task_info["task"]["title"], "Current Task")


if __name__ == '__main__':
    unittest.main()
