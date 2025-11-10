# Jules for Hugging Face - Main Entry Point

from .core.logic_engine import LogicEngine
from .tools.abstraction_layer import ToolAbstractionLayer
from .tools.file_system_manager import FileSystemManager
from .tools.git_client import GitClient
from .tools.huggingface_client import HuggingFaceClient
from .core.state_manager import StateManager
import os

def main():
    """
    Main function for the Jules for Hugging Face application.
    """
    print("Jules for Hugging Face - Initializing...")
    tool_layer = ToolAbstractionLayer()
    state_manager = StateManager()

    # Register tools
    tool_layer.register_tool("huggingface_client", HuggingFaceClient)

    # --- Login to Hugging Face ---
    print("--- Logging in to Hugging Face ---")
    hf_token = os.getenv("HUGGING_FACE_TOKEN")
    if not hf_token:
        print("Error: HUGGING_FACE_TOKEN environment variable not set.")
        return

    login_params = {"operation": "login", "token": hf_token}
    login_result = tool_layer.execute_tool("huggingface_client", login_params)
    print(f"Login Result: {login_result}")
    state_manager.update_state("I-2.2.1", "In Progress", f"Hugging Face login: {login_result}")


    # --- Create a new repository ---
    print("\n--- Creating a new repository on the Hub ---")
    repo_id = "jules-test-repo-123" # A unique name for the test repo
    create_repo_params = {"operation": "create_repo", "repo_id": repo_id}
    create_repo_result = tool_layer.execute_tool("huggingface_client", create_repo_params)
    print(f"Create Repo Result: {create_repo_result}")
    state_manager.update_state("I-2.2.1", "Completed", f"Repo creation: {create_repo_result}")


if __name__ == "__main__":
    main()
