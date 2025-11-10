# Jules for Hugging Face - Git Client Tool

import subprocess

class GitClient:
    """
    A tool for interacting with Git repositories.
    """

    def run(self, parameters: dict) -> str:
        """
        Runs the GitClient tool.
        Dispatches to the correct method based on the 'operation' parameter.
        """
        operation = parameters.get("operation")
        if operation == "clone":
            return self.clone(parameters)
        else:
            return f"Error: Unsupported operation '{operation}' for GitClient."

    def clone(self, parameters: dict) -> str:
        """
        Clones a Git repository.
        """
        repo_url = parameters.get("repo_url")
        if not repo_url:
            return "Error: 'repo_url' parameter is required for the clone operation."

        try:
            result = subprocess.run(
                ["git", "clone", repo_url],
                capture_output=True,
                text=True,
                check=True
            )
            return f"Successfully cloned repository: {repo_url}\n{result.stdout}"
        except subprocess.CalledProcessError as e:
            return f"Error cloning repository: {e}\n{e.stderr}"
        except FileNotFoundError:
            return "Error: 'git' command not found. Please ensure Git is installed and in your PATH."
