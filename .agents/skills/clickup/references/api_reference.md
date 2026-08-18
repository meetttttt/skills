# ClickUp MCP Tools & REST API v2 Reference

This document provides a detailed reference for ClickUp interactions via **MCP Tools (Priority 1)** and **REST API v2 (Priority 2 Fallback)**.

---

## 1. Priority 1: Native MCP Tools

When the ClickUp MCP server is active, agents invoke these native tools directly:

| Action | MCP Tool Name | Arguments |
| :--- | :--- | :--- |
| **Get Workspaces** | `clickup_get_workspaces` / `get_teams` | `{}` |
| **Get / Delete List** | `clickup_get_list` / `clickup_delete_list` | `{ "listId": "123" }` |
| **Create List** | `clickup_create_list` | `{ "spaceId": "123", "name": "Sprint 5" }` |
| **Get Task Details** | `clickup_get_task` | `{ "taskId": "CU-8675309" }` |
| **Create Task** | `clickup_create_task` | `{ "listId": "123", "name": "Task", "description": "...", "priority": 1 }` |
| **Delete Task** | `clickup_delete_task` | `{ "taskId": "CU-8675309" }` |
| **Update Task** | `clickup_update_task` | `{ "taskId": "CU-8675309", "status": "in review", "priority": 2 }` |
| **Assign / Reassign User** | `clickup_update_task` | `{ "taskId": "CU-8675309", "assignees": { "add": [123], "rem": [456] } }` |
| **Post Comment** | `clickup_create_comment` | `{ "taskId": "CU-8675309", "commentText": "..." }` |

---

## 2. Priority 2: REST API v2 Endpoints (Fallback)

Base URL: `https://api.clickup.com/api/v2` | Header: `Authorization: <CLICKUP_API_TOKEN>`

### Workspace & List Endpoints
- `GET /team`: Get user's workspaces.
- `GET /space/{space_id}/list`: Get lists in space.
- `POST /space/{space_id}/list`: Create list (Body: `{"name": "List Name"}`).
- `DELETE /list/{list_id}`: Delete list.

### Task Endpoints
- `GET /task/{task_id}`: Fetch task details directly by Task ID (No space/list required!).
- `GET /team/{team_id}/task?query=search_text`: Search tasks across workspace.
- `POST /list/{list_id}/task`: Create task (Body: `{"name": "...", "description": "...", "priority": 1, "assignees": [123]}`).
- `DELETE /task/{task_id}`: Delete task.
- `PUT /task/{task_id}`: Update task properties:
  - Status: `{"status": "in review"}`
  - Description: `{"description": "New content..."}` (or `""` to clear)
  - Priority: `{"priority": 1}` (1=Urgent, 2=High, 3=Normal, 4=Low, null=Clear)
  - Assignees: `{"assignees": {"add": [123], "rem": [456]}}`

---

## Priority Values in ClickUp

| Code | Label | Meaning |
| :--- | :--- | :--- |
| `1` | **Urgent** | Highest priority (Red) |
| `2` | **High** | High priority (Yellow) |
| `3` | **Normal** | Normal priority (Blue) |
| `4` | **Low** | Low priority (Grey) |
| `null` | **Clear / None** | Remove priority |
