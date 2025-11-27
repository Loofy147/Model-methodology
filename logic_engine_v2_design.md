# Logic Engine v2 - Design Document

## 1. Introduction

The current `LogicEngine` is a hardcoded placeholder that simulates LLM responses. This design proposes a production-ready `LogicEngineV2` that replaces the placeholder with a robust, state-driven architecture capable of integrating with a real Large Language Model (LLM). Its primary goal is to reliably decide the next action based on the project's state, available tools, and the current task.

## 2. Core Principles

-   **Single-Threaded Architecture:** The engine will follow a single-threaded, linear execution model ("thought -> action -> observation"). This is simpler to orchestrate and more reliable for the tightly-coupled tasks this agent performs (e.g., file system operations, git commands).
-   **State-Driven:** The agent's control loop will be stateless. A `state` dictionary will be passed into the engine for each turn, and the engine will return the next action to be taken. This makes the logic predictable and easy to test.
-   **Structured I/O:** The engine will communicate with the rest of the system via structured JSON objects, not strings. This eliminates fragile parsing and improves reliability.
-   **LLM Abstraction:** The specific LLM implementation will be abstracted behind a provider interface, allowing for different models (e.g., from Hugging Face, OpenAI, Anthropic) to be used without changing the core logic.

## 3. Proposed Architecture

### 3.1. `LogicEngineV2` Class

The new engine will be implemented in a class `LogicEngineV2`.

```python
class LogicEngineV2:
    def __init__(self, llm_provider: LLMProvider):
        self.llm_provider = llm_provider

    def get_next_action(self, state: dict) -> dict:
        # 1. Construct the prompt from the state
        # 2. Call the LLM provider
        # 3. Parse and validate the response
        # 4. Return a structured action object
        pass
```

### 3.2. The `state` Dictionary

This dictionary will be the single source of truth for the engine's decision-making process for a given turn.

```json
{
  "user_input": "What is the next step?",
  "current_task": {
    "id": "I-3.1.1",
    "title": "Implement the Methodology Engine",
    "status": "In Progress"
  },
  "available_tools": [
    {
      "name": "file_system_manager.create_file",
      "description": "Creates a new file at a specified path.",
      "parameters": {"file_path": "string", "content": "string"}
    },
    // ... other tools
  ],
  "short_term_memory": [
    {"role": "user", "content": "Let's start the implementation."},
    {"role": "assistant", "action": "execute_tool('file_system_manager.create_file', ...)"},
    {"role": "system", "observation": "File created successfully."}
  ]
}
```

### 3.3. The Control Loop (`get_next_action`)

The method will orchestrate the following steps:

1.  **Prompt Construction:** A detailed system prompt will be dynamically generated using the `state` dictionary. It will clearly define the agent's role, the current goal (from the task), the available tools (with schemas), the conversation history (from short-term memory), and the required JSON output format.
2.  **LLM Call:** The generated prompt will be sent to the configured `llm_provider`.
3.  **Response Parsing:** The LLM's response is expected to be a JSON object. The engine will parse this JSON and validate it against a known schema. If parsing or validation fails, it will trigger a retry or error-handling flow.
4.  **Action Return:** A structured dictionary representing the chosen action is returned.

### 3.4. Structured Action Format

The engine will return one of the following JSON objects:

-   **For tool execution:**
    ```json
    {
      "action": "execute_tool",
      "tool_name": "file_system_manager.create_file",
      "parameters": {
        "file_path": "src/main.py",
        "content": "# Start of the file"
      }
    }
    ```
-   **For user interaction:**
    ```json
    {
      "action": "ask_user",
      "question": "I have created the file. What should be the next step?"
    }
    ```
-   **For task completion:**
    ```json
    {
        "action": "complete_task",
        "final_message": "The implementation is complete as per the requirements."
    }
    ```

### 3.5. LLM Provider Interface

To keep the engine modular, we will define a simple interface that all LLM providers must implement.

```python
from abc import ABC, abstractmethod

class LLMProvider(ABC):
    @abstractmethod
    def get_structured_response(self, prompt: str) -> dict:
        """
        Sends a prompt to the LLM and returns a parsed JSON object.
        """
        pass
```

This allows us to easily swap out different models or APIs (e.g., `HuggingFaceLLM`, `OpenAILLM`).

## 4. Example Flow

1.  The main application loop constructs the `state` dictionary.
2.  It calls `logic_engine.get_next_action(state)`.
3.  The `LogicEngineV2` builds a detailed prompt and sends it to its `llm_provider`.
4.  The LLM provider returns a JSON string, e.g., `"{'action': 'execute_tool', 'tool_name': 'file_system_manager.create_file', ...}"`.
5.  The `LogicEngineV2` parses this string into a dictionary and returns it.
6.  The main application loop receives the action dictionary and calls the appropriate tool or user interaction function.
7.  The result of the action (e.g., "File created successfully") is added to the short-term memory for the next turn.
