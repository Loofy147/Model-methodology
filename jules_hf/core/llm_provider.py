# Jules for Hugging Face - LLM Provider Interface

from abc import ABC, abstractmethod
import json

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
    Returns a predefined response.
    """
    def __init__(self, response: dict):
        self.response = response

    def get_structured_response(self, prompt: str) -> dict:
        """
        Returns the mock response.
        """
        # In a real mock, you might want to log the prompt for inspection
        print(f"--- Mock LLM Prompt ---\n{prompt}\n-----------------------")
        return self.response
