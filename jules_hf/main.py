# Jules for Hugging Face - Main Entry Point

from .core.logic_engine import LogicEngine
from .tools.abstraction_layer import ToolAbstractionLayer
from .tools.file_system_manager import FileSystemManager
from .core.state_manager import StateManager

def main():
    """
    Main function for the Jules for Hugging Face application.
    """
    print("Jules for Hugging Face - Initializing...")
    engine = LogicEngine()
    tool_layer = ToolAbstractionLayer()
    state_manager = StateManager()

    # Register the FileSystemManager tool
    tool_layer.register_tool("file_system_manager.create_file", FileSystemManager)

    # Get the current task from the state manager
    current_task = state_manager.get_current_task()
    print(f"Current Task from State: {current_task}")


    user_input = "Please create a file named new_file.txt"
    state_manager.update_state("I-1.3.1", "In Progress", f"Processing user input: {user_input}")
    next_action = engine.get_next_action(user_input)
    print(f"User Input: '{user_input}'")
    print(f"Next Action: {next_action}")

    # This is a simplified parsing of the "next_action" string.
    if next_action.startswith("execute_tool"):
        # Simplified parsing for demonstration purposes
        tool_name = "file_system_manager.create_file"
        params = {'file_path': 'new_file.txt'}
        result = tool_layer.execute_tool(tool_name, params)
        print(f"Tool Execution Result: {result}")
        state_manager.update_state("I-1.3.1", "Completed", f"Tool executed successfully: {result}")

    print(f"Current Task from State: {state_manager.get_current_task()}")

if __name__ == "__main__":
    main()
