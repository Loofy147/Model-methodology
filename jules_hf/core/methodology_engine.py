# Jules for Hugging Face - Methodology Engine

import json
import os
from importlib import resources

class MethodologyEngine:
    """
    Loads and tracks the project's methodology from a plan file.
    """

    def __init__(self, plan_file_path: str = "plan.json"):
        """
        Initializes the MethodologyEngine.
        """
        self.plan = self._load_plan(plan_file_path)

    def _load_plan(self, plan_file_path: str) -> dict:
        """
        Loads the project plan from a JSON file within the package.
        """
        try:
            # Use importlib.resources to reliably find the file
            with resources.files('jules_hf').joinpath(plan_file_path).open('r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"error": f"Plan file not found at {plan_file_path}"}
        except json.JSONDecodeError:
            return {"error": "Invalid JSON in plan file."}

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
