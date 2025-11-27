# Jules for Hugging Face - LLM Provider Interface

from abc import ABC, abstractmethod
import json
from huggingface_hub import InferenceClient
from ..core.config import config
from ..core.exceptions import LLMError

class LLMProvider(ABC):
    """
    Abstract base class for LLM providers.
    """
    @abstractmethod
    def get_structured_response(self, prompt: str) -> dict:
        """
        Sends a prompt to the LLM and returns a parsed JSON object.
        """
        pass

class MockLLMProvider(LLMProvider):
    """
    A mock LLM provider for testing purposes.
    """
    def __init__(self, response: dict):
        self.response = response

    def get_structured_response(self, prompt: str) -> dict:
        """
        Returns the mock response and logs the prompt.
        """
        from .logging import get_logger
        logger = get_logger(__name__)
        logger.info("--- Mock LLM Prompt ---\\n%s\\n-----------------------", prompt)
        return self.response

class HuggingFaceLLMProvider(LLMProvider):
    """
    An LLM provider that uses the Hugging Face Inference API.
    """
    def __init__(self):
        model_id = config.get("llm", {}).get("model_id")
        if not model_id:
            raise LLMError("LLM model_id is not specified in the configuration.")

        self.client = InferenceClient()
        self.model_id = model_id

    def get_structured_response(self, prompt: str) -> dict:
        """
        Sends a prompt to the Hugging Face Inference API and returns a structured JSON response.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
            )

            content = response.choices[0].message.content
            if not content:
                raise LLMError("LLM returned an empty response.")

            return json.loads(content)

        except json.JSONDecodeError as e:
            raise LLMError(f"Failed to parse JSON response from LLM: {e}") from e
        except Exception as e:
            # General catch for API errors or other issues
            raise LLMError(f"An error occurred with the Hugging Face API: {e}") from e
