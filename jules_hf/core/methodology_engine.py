# Jules for Hugging Face - Methodology Engine

import json
import os
import shutil
from importlib import resources

class MethodologyEngine:
    """
    Loads and tracks the project's methodology from a user-writable plan file.
    """

    def __init__(self, user_dir: str = ".jules_hf", plan_filename: str = "plan.json"):
        """
        Initializes the MethodologyEngine.
        Sets up a user-writable directory for the plan if it doesn't exist.
        """
        self.user_dir = user_dir
        self.plan_file_path = os.path.join(self.user_dir, plan_filename)
        self.plan = self._load_plan()

    def _ensure_user_dir_exists(self):
        """
        Ensures the user-writable directory exists.
        """
        if not os.path.exists(self.user_dir):
            os.makedirs(self.user_dir)

    def _load_plan(self) -> dict:
        """
        Loads the project plan from the user-writable directory.
        If the plan doesn't exist, it's copied from the package resources.
        """
        self._ensure_user_dir_exists()

        if not os.path.exists(self.plan_file_path):
            self._copy_default_plan()

        try:
            with open(self.plan_file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            return {"error": str(e)}

    def _copy_default_plan(self):
        """
        Copies the default plan from package resources to the user directory.
        """
        try:
            with resources.files('jules_hf').joinpath('plan.json').open('rb') as src:
                with open(self.plan_file_path, 'wb') as dst:
                    shutil.copyfileobj(src, dst)
        except FileNotFoundError:
            # Create an empty plan if the default is missing for some reason
            with open(self.plan_file_path, 'w') as f:
                json.dump({"project_name": "New Project", "epics": []}, f)


    def get_current_task(self) -> dict:
        """
        Finds and returns the current 'Ready' or 'In Progress' task from the plan.
        """
        for epic in self.plan.get("epics", []):
            if epic.get("status") == "In Progress":
                for milestone in epic.get("milestones", []):
                    if milestone.get("status") == "In Progress":
                        for feature in milestone.get("features", []):
                            for task in feature.get("tasks", []):
                                if task.get("status") in ["Ready", "In Progress"]:
                                    return {
                                        "epic": epic.get("id"),
                                        "milestone": milestone.get("id"),
                                        "task": task
                                    }
        return {"task": {"id": None, "title": "No current task found."}}

    def update_task_status(self, task_id: str, status: str) -> bool:
        """
        Updates the status of a specific task and saves the plan.
        """
        task_found = False
        for epic in self.plan.get("epics", []):
            for milestone in epic.get("milestones", []):
                for feature in milestone.get("features", []):
                    for task in feature.get("tasks", []):
                        if task.get("id") == task_id:
                            task["status"] = status
                            task_found = True
                            break
                    if task_found:
                        break
                if task_found:
                    break
            if task_found:
                break

        if task_found:
            self._save_plan()

        return task_found

    def _save_plan(self):
        """
        Saves the current plan back to the user-writable file.
        """
        self._ensure_user_dir_exists()
        with open(self.plan_file_path, 'w') as f:
            json.dump(self.plan, f, indent=4)
