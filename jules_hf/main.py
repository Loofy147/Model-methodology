# Jules for Hugging Face - Main Entry Point

import re
import ast
from .core.logic_engine import LogicEngine
from .core.methodology_engine import MethodologyEngine
from .tools.abstraction_layer import ToolAbstractionLayer
from .tools.file_system_manager import FileSystemManager
from .tools.git_client import GitClient
from .tools.huggingface_client import HuggingFaceClient

class JulesHF:
    """
    The main application class for Jules for Hugging Face.
    """
    def __init__(self):
        self.logic_engine = LogicEngine()
        self.methodology_engine = MethodologyEngine()
        self.tool_layer = ToolAbstractionLayer()
        self._register_tools()

    def _register_tools(self):
        self.tool_layer.register_tool("file_system_manager", FileSystemManager)
        self.tool_layer.register_tool("git_client", GitClient)
        self.tool_layer.register_tool("huggingface_client", HuggingFaceClient)

    def run(self):
        print("Jules for Hugging Face - Running...")
        current_task_info = self.methodology_engine.get_current_task()

        print("\n--- Current Task ---")
        task = current_task_info.get('task', {})
        print(f"Task Title: {task.get('title')}")

        user_input = "What is the next step for the current task?"
        next_action = self.logic_engine.get_next_action(user_input, current_task_info)

        print("\n--- Next Action ---")
        print(next_action)
        self._execute_action(next_action)

    def _execute_action(self, action_string: str):
        if not action_string.startswith("execute_tool"):
            print(f"Action not executable: {action_string}")
            return

        match = re.search(r"execute_tool\('([^']*)',\s*({.*})\)", action_string)
        if match:
            tool_name, params_str = match.groups()
            try:
                params = ast.literal_eval(params_str)
                result = self.tool_layer.execute_tool(tool_name, params)
                print("\n--- Tool Execution Result ---")
                print(result)
            except (ValueError, SyntaxError) as e:
                print(f"Error parsing parameters: {e}")

def main():
    """
    Main entry point for the application.
    """
    app = JulesHF()
    app.run()

if __name__ == "__main__":
    main()
