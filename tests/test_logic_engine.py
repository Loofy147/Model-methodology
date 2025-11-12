# tests/test_logic_engine.py

import unittest
from jules_hf.core.logic_engine import LogicEngine

class TestLogicEngine(unittest.TestCase):
    """
    Unit tests for the LogicEngine class.
    """

    def setUp(self):
        """
        Set up the test case.
        """
        self.engine = LogicEngine()
        self.mock_task = {
            "task": {
                "id": "Test-Task",
                "title": "Implement the Methodology Engine"
            }
        }

    def test_get_next_action_with_task_context(self):
        """
        Test that the LogicEngine uses the task context to make a decision.
        """
        user_input = "What should I do now?"
        expected_action = "execute_tool('file_system_manager.create_file', {'file_path': 'implementation_notes.txt'})"
        actual_action = self.engine.get_next_action(user_input, self.mock_task)
        self.assertEqual(actual_action, expected_action)

    def test_get_next_action_unknown_intent(self):
        """
        Test that the LogicEngine returns the 'clarification' action for unknown intents.
        """
        user_input = "What is the weather today?"
        mock_task_other = {"task": {"title": "Some other task"}}
        expected_action = "prompt_user_for_clarification"
        actual_action = self.engine.get_next_action(user_input, mock_task_other)
        self.assertEqual(actual_action, expected_action)

if __name__ == '__main__':
    unittest.main()
