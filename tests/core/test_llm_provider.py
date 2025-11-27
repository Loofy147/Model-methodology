# tests/core/test_llm_provider.py

import unittest
from unittest.mock import patch, MagicMock
from jules_hf.core.llm_provider import HuggingFaceLLMProvider
from jules_hf.core.exceptions import LLMError
from jules_hf.core.config import config

class TestHuggingFaceLLMProvider(unittest.TestCase):
    """
    Unit tests for the HuggingFaceLLMProvider class.
    """

    @patch('jules_hf.core.llm_provider.InferenceClient')
    def test_get_structured_response_success(self, MockInferenceClient):
        """
        Test that the provider returns a parsed JSON object on a successful API call.
        """
        # Mock the API response
        mock_api_response = MagicMock()
        mock_api_response.choices[0].message.content = '{"action": "test"}'

        # Configure the mock client instance
        mock_client_instance = MockInferenceClient.return_value
        mock_client_instance.chat.completions.create.return_value = mock_api_response

        # Instantiate the provider
        with patch.dict(config.settings, {"llm": {"model_id": "test-model"}}):
            provider = HuggingFaceLLMProvider()
            response = provider.get_structured_response("test prompt")

        self.assertEqual(response, {"action": "test"})
        mock_client_instance.chat.completions.create.assert_called_once()

    @patch('jules_hf.core.llm_provider.InferenceClient')
    def test_api_error_raises_llm_error(self, MockInferenceClient):
        """
        Test that an API error raises an LLMError.
        """
        mock_client_instance = MockInferenceClient.return_value
        mock_client_instance.chat.completions.create.side_effect = Exception("API is down")

        with patch.dict(config.settings, {"llm": {"model_id": "test-model"}}):
            provider = HuggingFaceLLMProvider()
            with self.assertRaises(LLMError):
                provider.get_structured_response("test prompt")

    @patch('jules_hf.core.llm_provider.InferenceClient')
    def test_invalid_json_raises_llm_error(self, MockInferenceClient):
        """
        Test that an invalid JSON response from the LLM raises an LLMError.
        """
        mock_api_response = MagicMock()
        mock_api_response.choices[0].message.content = '{"action": "test",}' # Invalid JSON

        mock_client_instance = MockInferenceClient.return_value
        mock_client_instance.chat.completions.create.return_value = mock_api_response

        with patch.dict(config.settings, {"llm": {"model_id": "test-model"}}):
            provider = HuggingFaceLLMProvider()
            with self.assertRaises(LLMError):
                provider.get_structured_response("test prompt")

    def test_missing_model_id_raises_error(self):
        """
        Test that a missing model_id in the config raises an LLMError.
        """
        with patch.dict(config.settings, {"llm": {}}): # Missing model_id
            with self.assertRaises(LLMError):
                HuggingFaceLLMProvider()

if __name__ == '__main__':
    unittest.main()
