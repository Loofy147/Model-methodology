# Jules for Hugging Face - Hugging Face Client Tool

import os
from huggingface_hub import HfApi, create_repo, login
from ..core.exceptions import ConfigurationError, ToolExecutionError

class HuggingFaceClient:
    """
    A tool for interacting with the Hugging Face Hub.
    Loads the API token from the HUGGING_FACE_HUB_TOKEN environment variable.
    """

    def __init__(self):
        self.token = os.getenv("HUGGING_FACE_HUB_TOKEN")
        if not self.token:
            raise ConfigurationError("HUGGING_FACE_HUB_TOKEN environment variable not set.")
        self.api = HfApi()

    def run(self, parameters: dict) -> str:
        """
        Runs the HuggingFaceClient tool.
        Dispatches to the correct method based on the 'operation' parameter.
        """
        operation = parameters.get("operation")
        if operation == "login":
            return self.login()
        elif operation == "create_repo":
            return self.create_repo(parameters)
        else:
            raise ToolExecutionError(f"Unsupported operation '{operation}' for HuggingFaceClient.")

    def login(self) -> str:
        """
        Logs in to the Hugging Face Hub using the token from the environment.
        """
        try:
            login(token=self.token, add_to_git_credential=True)
            return "Successfully logged in to the Hugging Face Hub."
        except Exception as e:
            raise ToolExecutionError(f"Failed to log in to Hugging Face Hub: {e}") from e

    def create_repo(self, parameters: dict) -> str:
        """
        Creates a new repository on the Hugging Face Hub.
        """
        repo_id = parameters.get("repo_id")
        if not repo_id:
            raise ToolExecutionError("'repo_id' parameter is required for the create_repo operation.")

        repo_type = parameters.get("repo_type", "model")

        try:
            repo_url = create_repo(repo_id=repo_id, repo_type=repo_type, token=self.token)
            return f"Successfully created repository: {repo_url}"
        except Exception as e:
            raise ToolExecutionError(f"Failed to create repository '{repo_id}': {e}") from e
