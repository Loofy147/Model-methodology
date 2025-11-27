# Jules for Hugging Face - Methodology Engine

import json
import os
import shutil
from importlib import resources
from .config import config
from .logging import get_logger

logger = get_logger(__name__)

class MethodologyEngine:
    """
    Loads and tracks the project's methodology from a user-writable plan file.
    """

    def __init__(self):
        """
        Initializes the MethodologyEngine.
        """
        logger.info("Initializing MethodologyEngine...")
        user_dir = config.get("user_data_dir", ".jules_hf")
        plan_filename = config.get("plan_filename", "plan.json")
        self.user_dir = user_dir
        self.plan_file_path = os.path.join(self.user_dir, plan_filename)
        self.plan = self._load_plan()
        logger.info("MethodologyEngine initialized.")

    def _ensure_user_dir_exists(self):
        """
        Ensures the user-writable directory exists.
        """
        if not os.path.exists(self.user_dir):
            logger.info(f"User directory not found. Creating at: {self.user_dir}")
            os.makedirs(self.user_dir)

    def _load_plan(self) -> dict:
        """
        Loads the project plan from the user-writable directory.
        """
        self._ensure_user_dir_exists()

        if not os.path.exists(self.plan_file_path):
            logger.info(f"Plan file not found at {self.plan_file_path}. Copying default plan.")
            self._copy_default_plan()

        logger.debug(f"Loading plan from {self.plan_file_path}")
        try:
            with open(self.plan_file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"Failed to load plan file: {e}", exc_info=True)
            return {"error": str(e)}

    def _copy_default_plan(self):
        """
        Copies the default plan from package resources to the user directory.
        """
        try:
            with resources.files('jules_hf').joinpath('plan.json').open('rb') as src:
                with open(self.plan_file_path, 'wb') as dst:
                    shutil.copyfileobj(src, dst)
            logger.info(f"Successfully copied default plan to {self.plan_file_path}")
        except FileNotFoundError:
            logger.warning("Default 'plan.json' not found in package. Creating an empty plan.")
            with open(self.plan_file_path, 'w') as f:
                json.dump({"project_name": "New Project", "epics": []}, f)

    def get_current_task(self) -> dict:
        """
        Finds and returns the current 'Ready' or 'In Progress' task from the plan.
        """
        logger.debug("Searching for the current task...")
        # ... (rest of the method is unchanged)
        for epic in self.plan.get("epics", []):
            if epic.get("status") == "In Progress":
                for milestone in epic.get("milestones", []):
                    if milestone.get("status") == "In Progress":
                        for feature in milestone.get("features", []):
                            for task in feature.get("tasks", []):
                                if task.get("status") in ["Ready", "In Progress"]:
                                    logger.debug(f"Current task found: {task.get('id')}")
                                    return {
                                        "epic": epic.get("id"),
                                        "milestone": milestone.get("id"),
                                        "task": task
                                    }
        logger.warning("No current task found in the plan.")
        return {"task": {"id": None, "title": "No current task found."}}

    def update_task_status(self, task_id: str, status: str) -> bool:
        """
        Updates the status of a specific task and saves the plan.
        """
        logger.debug(f"Attempting to update task '{task_id}' to status '{status}'.")
        task_found = False
        # ... (loop logic is unchanged)
        for epic in self.plan.get("epics", []):
            for milestone in epic.get("milestones", []):
                for feature in milestone.get("features", []):
                    for task in feature.get("tasks", []):
                        if task.get("id") == task_id:
                            task["status"] = status
                            task_found = True
                            break
                    if task_found: break
                if task_found: break
            if task_found: break

        if task_found:
            logger.info(f"Task '{task_id}' status updated to '{status}'. Saving plan.")
            self._save_plan()
        else:
            logger.warning(f"Task '{task_id}' not found. Could not update status.")

        return task_found

    def _save_plan(self):
        """
        Saves the current plan back to the user-writable file.
        """
        logger.debug(f"Saving plan to {self.plan_file_path}")
        self._ensure_user_dir_exists()
        try:
            with open(self.plan_file_path, 'w') as f:
                json.dump(self.plan, f, indent=4)
            logger.info("Plan saved successfully.")
        except IOError as e:
            logger.error(f"Failed to save plan: {e}", exc_info=True)
