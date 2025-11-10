# Jules for Hugging Face - State Manager

import json
import os

class StateManager:
    """
    Manages the state of the project, allowing the agent to resume tasks.
    """

    def __init__(self, state_file_path: str = "project_state.json"):
        """
        Initializes the StateManager.
        """
        self.state_file_path = state_file_path
        self.state = self._load_state()

    def _load_state(self) -> dict:
        """
        Loads the project state from the state file.
        """
        if os.path.exists(self.state_file_path):
            with open(self.state_file_path, "r") as f:
                return json.load(f)
        else:
            return {"current_task_id": None, "history": []}

    def save_state(self):
        """
        Saves the current project state to the state file.
        """
        with open(self.state_file_path, "w") as f:
            json.dump(self.state, f, indent=4)

    def update_state(self, task_id: str, status: str, details: str):
        """
        Updates the state with the latest task information.
        """
        self.state["current_task_id"] = task_id
        self.state["history"].append({
            "task_id": task_id,
            "status": status,
            "details": details
        })
        self.save_state()

    def get_current_task(self) -> str:
        """
        Returns the ID of the current task.
        """
        return self.state.get("current_task_id")
