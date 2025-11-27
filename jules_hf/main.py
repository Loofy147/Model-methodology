# Jules for Hugging Face - Main Entry Point

from .core.logic_engine_v2 import LogicEngineV2
from .core.llm_provider import MockLLMProvider
from .core.methodology_engine import MethodologyEngine
from .tools.abstraction_layer import ToolAbstractionLayer
from .tools.file_system_manager import FileSystemManager
from .tools.git_client import GitClient
from .tools.huggingface_client import HuggingFaceClient
from .core.logging import setup_logging, get_logger
from .core.exceptions import ToolExecutionError, LLMError

# Initialize logger for this module
logger = get_logger(__name__)

class JulesHF:
    """
    The main application class for Jules for Hugging Face.
    """
    def __init__(self):
        logger.info("Initializing JulesHF application...")

        # Using MockLLMProvider for now. This would be configurable in a real app.
        mock_response = {
            "action": "execute_tool",
            "tool_name": "file_system_manager.create_file",
            "parameters": {"file_path": "test_output.txt", "content": "Hello from LogicEngineV2!"}
        }
        llm_provider = MockLLMProvider(response=mock_response)

        self.logic_engine = LogicEngineV2(llm_provider)
        self.methodology_engine = MethodologyEngine()
        self.tool_layer = ToolAbstractionLayer()
        self.short_term_memory = []

        self._register_tools()
        logger.info("JulesHF application initialized successfully.")

    def _register_tools(self):
        self.tool_layer.register_tool("file_system_manager", FileSystemManager)
        self.tool_layer.register_tool("git_client", GitClient)
        # self.tool_layer.register_tool("huggingface_client", HuggingFaceClient) # Mocked for now
        logger.debug("All tools registered.")

    def run(self):
        logger.info("JulesHF run started.")

        current_task_info = self.methodology_engine.get_current_task()
        task = current_task_info.get('task', {})
        logger.info("Current task retrieved.", extra={'extra_context': {'task_id': task.get('id'), 'task_title': task.get('title')}})

        # The main loop would be more sophisticated in a real agent
        self._run_single_turn()

        logger.info("JulesHF run finished.")

    def _run_single_turn(self):
        """
        Runs a single turn of the agent's thought-action loop.
        """
        state = self._build_current_state()

        try:
            action = self.logic_engine.get_next_action(state)
            self._execute_action(action)
        except (ToolExecutionError, LLMError) as e:
            logger.error(f"A recoverable error occurred: {e}", exc_info=True)
            # In a real agent, we might add this error to memory and retry
        except Exception as e:
            logger.critical(f"An unrecoverable error occurred: {e}", exc_info=True)

    def _build_current_state(self) -> dict:
        """
        Constructs the current state dictionary to be passed to the LogicEngine.
        """
        return {
            "current_task": self.methodology_engine.get_current_task().get('task', {}),
            "available_tools": self.tool_layer.get_tools(), # In a real system, this would be more dynamic
            "short_term_memory": self.short_term_memory
        }

    def _execute_action(self, action: dict):
        action_type = action.get("action")
        logger.info(f"Executing action: {action_type}", extra={'extra_context': {'action': action}})

        if action_type == "execute_tool":
            tool_name = action.get("tool_name")
            parameters = action.get("parameters")
            result = self.tool_layer.execute_tool(tool_name, parameters)

            # Update memory with the result
            self.short_term_memory.append({"role": "assistant", "action": action})
            self.short_term_memory.append({"role": "system", "observation": result})

        elif action_type == "ask_user":
            question = action.get("question")
            logger.info(f"Asking user: {question}")
            # In a real app, this would pause and wait for user input

        elif action_type == "complete_task":
            message = action.get("final_message")
            logger.info(f"Task completed with message: {message}")
            # Here you would update the methodology engine
            # self.methodology_engine.update_task_status(...)

        else:
            logger.error(f"Unknown action type: {action_type}")


def main():
    """
    Main entry point for the application.
    """
    setup_logging()

    logger.info("Application starting...")
    try:
        app = JulesHF()
        app.run()
    except Exception as e:
        logger.critical(f"An unhandled exception caused the application to terminate: {e}", exc_info=True)
    finally:
        logger.info("Application finished.")

if __name__ == "__main__":
    main()
