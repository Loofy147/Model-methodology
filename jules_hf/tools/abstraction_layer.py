# Jules for Hugging Face - Tool Abstraction Layer

from ..core.logging import get_logger
from ..core.exceptions import ToolExecutionError

logger = get_logger(__name__)

class ToolAbstractionLayer:
    """
    The Tool Abstraction Layer is responsible for discovering and executing tools.
    """

    def __init__(self):
        """
        Initializes the ToolAbstractionLayer.
        """
        self._tools = {}
        logger.info("ToolAbstractionLayer initialized.")

    def register_tool(self, tool_name: str, tool_class):
        """
        Registers a new tool.
        """
        self._tools[tool_name] = tool_class()
        logger.info(f"Tool '{tool_name}' registered.", extra={'tool_name': tool_name, 'class': tool_class.__name__})

    def get_tools(self):
        """
        Returns a list of available tools.
        """
        logger.debug("Retrieving list of available tools.")
        return list(self._tools.keys())

    def execute_tool(self, tool_name: str, parameters: dict) -> str:
        """
        Executes a tool with the given parameters, raising exceptions on failure.
        """
        logger.debug(f"Attempting to execute tool '{tool_name}'.", extra={'tool_name': tool_name, 'parameters': parameters})

        if tool_name not in self._tools:
            msg = f"Tool '{tool_name}' not found."
            logger.error(msg)
            raise ToolExecutionError(msg)

        tool = self._tools[tool_name]

        if not hasattr(tool, "run"):
            msg = f"Tool '{tool_name}' does not have a 'run' method."
            logger.error(msg)
            raise ToolExecutionError(msg)

        try:
            result = tool.run(parameters)
            logger.info(f"Tool '{tool_name}' executed successfully.", extra={'tool_name': tool_name})
            return result
        except Exception as e:
            logger.error(f"An unexpected error occurred while executing tool '{tool_name}': {e}", exc_info=True, extra={'tool_name': tool_name})
            # Wrap the original exception to provide a consistent error type
            raise ToolExecutionError(f"Execution of tool '{tool_name}' failed: {e}") from e
