# Jules for Hugging Face - Logic Engine V2

from .llm_provider import LLMProvider
from .exceptions import LLMError
import json

class LogicEngineV2:
    """
    The second iteration of the core logic engine, designed for production readiness.
    """

    def __init__(self, llm_provider: LLMProvider):
        self.llm_provider = llm_provider

    def get_next_action(self, state: dict) -> dict:
        """
        Takes the current system state and returns the next action.
        """
        prompt = self._construct_prompt(state)

        try:
            response = self.llm_provider.get_structured_response(prompt)
        except Exception as e:
            raise LLMError(f"Error getting response from LLM provider: {e}") from e

        if not self._validate_response(response):
            raise LLMError("Invalid response format from LLM.")

        return response

    def _construct_prompt(self, state: dict) -> str:
        """
        Constructs a detailed prompt for the LLM based on the current state.
        """
        # This is a simplified example. A real implementation would be more sophisticated.
        prompt = f"""
You are Jules, a skilled software engineering assistant. Your goal is to complete the following task:
**Task:** {state.get('current_task', {}).get('title', 'No task specified.')}

**Available Tools:**
{json.dumps(state.get('available_tools', []), indent=2)}

**Conversation History:**
{json.dumps(state.get('short_term_memory', []), indent=2)}

Based on the task and history, what is the next logical action? Your response must be a single JSON object with one of the following structures:
1. To execute a tool: {{"action": "execute_tool", "tool_name": "...", "parameters": {{...}}}}
2. To ask the user a question: {{"action": "ask_user", "question": "..."}}
3. To complete the task: {{"action": "complete_task", "final_message": "..."}}
"""
        return prompt.strip()

    def _validate_response(self, response: dict) -> bool:
        """
        Validates the structure of the LLM's response.
        """
        if not isinstance(response, dict):
            return False

        action = response.get("action")
        if action not in ["execute_tool", "ask_user", "complete_task"]:
            return False

        if action == "execute_tool" and ("tool_name" not in response or "parameters" not in response):
            return False

        if action == "ask_user" and "question" not in response:
            return False

        if action == "complete_task" and "final_message" not in response:
            return False

        return True
