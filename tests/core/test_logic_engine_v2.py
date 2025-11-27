# tests/core/test_logic_engine_v2.py

import unittest
from jules_hf.core.logic_engine_v2 import LogicEngineV2
from jules_hf.core.llm_provider import MockLLMProvider
from jules_hf.core.exceptions import LLMError

class TestLogicEngineV2(unittest.TestCase):
    """
    Unit tests for the LogicEngineV2 class.
    """

    def setUp(self):
        """
        Set up a basic state for testing.
        """
        self.test_state = {
            "current_task": {"id": "T1", "title": "Test Task"},
            "available_tools": [{"name": "test_tool", "description": "A tool for testing."}],
            "short_term_memory": []
        }

    def test_get_next_action_success(self):
        """
        Test that the engine correctly returns a valid action from the LLM.
        """
        mock_response = {
            "action": "execute_tool",
            "tool_name": "test_tool",
            "parameters": {"param": "value"}
        }
        llm_provider = MockLLMProvider(response=mock_response)
        engine = LogicEngineV2(llm_provider)

        action = engine.get_next_action(self.test_state)
        self.assertEqual(action, mock_response)

    def test_invalid_response_from_llm_raises_error(self):
        """
        Test that the engine raises an LLMError if the response is invalid.
        """
        # Test with a completely invalid structure
        llm_provider = MockLLMProvider(response={"invalid": "response"})
        engine = LogicEngineV2(llm_provider)
        with self.assertRaises(LLMError):
            engine.get_next_action(self.test_state)

        # Test with a missing required field
        mock_response = {"action": "execute_tool", "parameters": {}} # Missing 'tool_name'
        llm_provider = MockLLMProvider(response=mock_response)
        engine = LogicEngineV2(llm_provider)
        with self.assertRaises(LLMError):
            engine.get_next_action(self.test_state)

    def test_llm_provider_exception_is_handled(self):
        """
        Test that exceptions from the LLM provider are caught and wrapped.
        """
        # Create a mock provider that raises an exception
        class FailingLLMProvider(MockLLMProvider):
            def get_structured_response(self, prompt: str) -> dict:
                raise ValueError("LLM API is down")

        llm_provider = FailingLLMProvider(response={})
        engine = LogicEngineV2(llm_provider)

        with self.assertRaises(LLMError):
            engine.get_next_action(self.test_state)


if __name__ == '__main__':
    unittest.main()
