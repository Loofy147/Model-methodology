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

    def test_get_next_action_create_file(self):
        """
        Test that the LogicEngine correctly identifies the 'create_file' intent.
        """
        user_input = "Please create a file named my_file.txt"
        expected_action = "execute_tool('file_system_manager.create_file', {'file_path': 'new_file.txt'})"
        actual_action = self.engine.get_next_action(user_input)
        self.assertEqual(actual_action, expected_action)

    def test_get_next_action_unknown_intent(self):
        """
        Test that the LogicEngine returns the 'clarification' action for unknown intents.
        """
        user_input = "What is the weather today?"
        expected_action = "prompt_user_for_clarification"
        actual_action = self.engine.get_next_action(user_input)
        self.assertEqual(actual_action, expected_action)

if __name__ == '__main__':
    unittest.main()
