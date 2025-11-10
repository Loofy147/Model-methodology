# Jules for Hugging Face - Hugging Face Client Tool

from huggingface_hub import HfApi, create_repo, login

class HuggingFaceClient:
    """
    A tool for interacting with the Hugging Face Hub.
    """

    def __init__(self):
        self.api = HfApi()

    def run(self, parameters: dict) -> str:
        """
        Runs the HuggingFaceClient tool.
        Dispatches to the correct method based on the 'operation' parameter.
        """
        operation = parameters.get("operation")
        if operation == "login":
            return self.login(parameters)
        elif operation == "create_repo":
            return self.create_repo(parameters)
        else:
            return f"Error: Unsupported operation '{operation}' for HuggingFaceClient."

    def login(self, parameters: dict) -> str:
        """
        Logs in to the Hugging Face Hub.
        """
        token = parameters.get("token")
        if not token:
            return "Error: 'token' parameter is required for the login operation."

        try:
            login(token=token, add_to_git_credential=True)
            return "Successfully logged in to the Hugging Face Hub."
        except Exception as e:
            return f"Error logging in: {e}"

    def create_repo(self, parameters: dict) -> str:
        """
        Creates a new repository on the Hugging Face Hub.
        """
        repo_id = parameters.get("repo_id")
        if not repo_id:
            return "Error: 'repo_id' parameter is required for the create_repo operation."

        repo_type = parameters.get("repo_type", "model") # default to model repo

        try:
            repo_url = create_repo(repo_id=repo_id, repo_type=repo_type)
            return f"Successfully created repository: {repo_url}"
        except Exception as e:
            return f"Error creating repository: {e}"
