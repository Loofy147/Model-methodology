# API Specification v1 (Task P-2.1.2)

This document defines the primary API contracts for the "Jules for Hugging Face" system, based on the architecture defined in `architecture_diagram_v1.md`.

---

### **1. Core Logic <-> Tool Abstraction Layer**

This is the most critical API, defining how the agent executes actions.

#### **Endpoint: `POST /tools/execute`**
-   **Description:** The Core Logic Engine calls this endpoint to execute a specific tool.
-   **Request Body:**
    ```json
    {
      "tool_name": "string",
      "parameters": {
        "param_name": "param_value"
      }
    }
    ```
-   **Response (Success):**
    ```json
    {
      "status": "success",
      "result": "The output from the tool execution.",
      "artifacts_generated": ["path/to/artifact.md"]
    }
    ```

#### **Endpoint: `GET /tools`**
-   **Description:** The Core Logic Engine queries this to discover the available tools and their schemas, allowing for dynamic capabilities.
-   **Response:**
    ```json
    {
      "tools": [
        {
          "name": "huggingface.list_models",
          "description": "Lists models on the Hugging Face Hub.",
          "parameters": { "search": "string" }
        },
        {
          "name": "git.commit",
          "description": "Commits changes to the local repository.",
          "parameters": { "message": "string" }
        }
      ]
    }
    ```

---

### **2. Core Logic <-> Methodology Engine**

This API ensures the agent adheres to our defined project lifecycle.

#### **Endpoint: `GET /methodology/state`**
-   **Description:** Retrieves the current state of the project.
-   **Response:**
    ```json
    {
        "current_epic": "Plan",
        "current_task_id": "P-2.1.2",
        "is_task_complete": false,
        "required_artifacts": ["API Specification v1"]
    }
    ```

#### **Endpoint: `POST /methodology/task/update`**
-   **Description:** Updates the status of a task.
-   **Request Body:**
    ```json
    {
        "task_id": "P-2.1.2",
        "status": "In Progress"
    }
    ```
-   **Response:**
    ```json
    { "status": "success" }
    ```
---
