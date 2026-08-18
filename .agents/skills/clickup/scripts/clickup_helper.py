#!/usr/bin/env python3
"""
ClickUp API v2 CLI Helper Script for AI Coding Agents and Developers.
Uses Python standard library (urllib) to require zero external dependencies.

Requirements:
    Environment variable: CLICKUP_API_TOKEN

Supported Commands:
    Workspaces & Lists:
        python3 clickup_helper.py get-workspaces
        python3 clickup_helper.py get-spaces <workspace_id>
        python3 clickup_helper.py get-lists <space_id>
        python3 clickup_helper.py create-list <space_id> "List Name"
        python3 clickup_helper.py delete-list <list_id>

    Task Operations:
        python3 clickup_helper.py get <task_id>
        python3 clickup_helper.py search-tasks <workspace_id> [query_text]
        python3 clickup_helper.py create-task <list_id> "Title" ["Description"] [priority 1-4] [assignee_id]
        python3 clickup_helper.py create-subtask <list_id> <parent_task_id> "Subtask Title" ["Description"]
        python3 clickup_helper.py delete-task <task_id>
        python3 clickup_helper.py update-status <task_id> "in review"
        python3 clickup_helper.py update-description <task_id> "New description..."
        python3 clickup_helper.py clear-description <task_id>
        python3 clickup_helper.py set-priority <task_id> <1|2|3|4|urgent|high|normal|low|clear>
        python3 clickup_helper.py assign-user <task_id> <user_id>
        python3 clickup_helper.py remove-user <task_id> <user_id>
        python3 clickup_helper.py reassign-user <task_id> <old_user_id> <new_user_id>
        python3 clickup_helper.py add-comment <task_id> "Comment text..."

    PRD / FRD Integration:
        python3 clickup_helper.py create-from-doc <doc_filepath> <list_id>
"""

import sys
import os
import re
import json
import urllib.request
import urllib.parse
import urllib.error

BASE_URL = "https://api.clickup.com/api/v2"

PRIORITY_MAP = {
    "1": 1, "urgent": 1,
    "2": 2, "high": 2,
    "3": 3, "normal": 3,
    "4": 4, "low": 4,
    "clear": None, "none": None
}

def get_api_token():
    token = os.environ.get("CLICKUP_API_TOKEN")
    if not token:
        print("Error: CLICKUP_API_TOKEN environment variable is not set.", file=sys.stderr)
        print("Please set it via: export CLICKUP_API_TOKEN='your_api_token'", file=sys.stderr)
        sys.exit(1)
    return token

def clean_task_id(task_id: str) -> str:
    """Normalize task ID by removing leading hashes or 'CU-' prefixes if present."""
    task_id = task_id.strip()
    if task_id.startswith("#"):
        task_id = task_id[1:]
    if task_id.lower().startswith("cu-"):
        task_id = task_id[3:]
    return task_id

def make_request(method: str, endpoint: str, payload: dict = None):
    token = get_api_token()
    url = f"{BASE_URL}{endpoint}"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method.upper())
    
    try:
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode("utf-8")
            return json.loads(res_body) if res_body else {}
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"HTTP Error {e.code}: {e.reason}", file=sys.stderr)
        print(f"Response: {error_body}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Request Error: {e}", file=sys.stderr)
        sys.exit(1)

# === Workspace & List Commands ===

def cmd_get_workspaces():
    data = make_request("GET", "/team")
    teams = data.get("teams", [])
    print("=== ClickUp Workspaces (Teams) ===")
    for t in teams:
        print(f"ID: {t.get('id')} | Name: {t.get('name')}")

def cmd_get_spaces(workspace_id: str):
    data = make_request("GET", f"/team/{workspace_id}/space")
    spaces = data.get("spaces", [])
    print(f"=== Spaces in Workspace {workspace_id} ===")
    for s in spaces:
        print(f"ID: {s.get('id')} | Name: {s.get('name')}")

def cmd_get_lists(space_id: str):
    data = make_request("GET", f"/space/{space_id}/list")
    lists = data.get("lists", [])
    print(f"=== Lists in Space {space_id} ===")
    for l in lists:
        print(f"ID: {l.get('id')} | Name: {l.get('name')} | Task Count: {l.get('task_count', 'N/A')}")

def cmd_create_list(space_id: str, name: str):
    payload = {"name": name}
    data = make_request("POST", f"/space/{space_id}/list", payload)
    print(f"Successfully created List '{data.get('name')}' (ID: {data.get('id')})")

def cmd_delete_list(list_id: str):
    make_request("DELETE", f"/list/{list_id}")
    print(f"Successfully deleted List {list_id}")

# === Task Commands ===

def cmd_get_task(task_id: str):
    tid = clean_task_id(task_id)
    data = make_request("GET", f"/task/{tid}")
    
    priority_info = data.get('priority') or {}
    p_name = priority_info.get('priority', 'None').upper()
    
    print(f"=== ClickUp Task Details ({data.get('id')}) ===")
    print(f"Title       : {data.get('name')}")
    print(f"Status      : {data.get('status', {}).get('status', 'N/A').upper()}")
    print(f"Priority    : {p_name}")
    print(f"URL         : {data.get('url')}")
    
    assignees = [f"{a.get('username') or a.get('email')} (ID: {a.get('id')})" for a in data.get('assignees', [])]
    print(f"Assignees   : {', '.join(assignees) if assignees else 'Unassigned'}")
    
    print("\n--- Description ---")
    print(data.get('text_content') or data.get('description') or "(No description provided)")
    print("==========================================")

def cmd_search_tasks(workspace_id: str, query: str = ""):
    endpoint = f"/team/{workspace_id}/task?subtasks=true"
    if query:
        endpoint += f"&query={urllib.parse.quote(query)}"
    data = make_request("GET", endpoint)
    tasks = data.get("tasks", [])
    print(f"=== Found {len(tasks)} tasks matching '{query}' ===")
    for t in tasks:
        p = (t.get('priority') or {}).get('priority', 'none')
        print(f"[{t.get('id')}] ({t.get('status', {}).get('status').upper()}) [{p.upper()}] {t.get('name')}")

def cmd_create_task(list_id: str, title: str, description: str = "", priority: str = None, assignee_id: str = None):
    payload = {"name": title, "description": description}
    if priority and priority.lower() in PRIORITY_MAP:
        payload["priority"] = PRIORITY_MAP[priority.lower()]
    if assignee_id:
        try:
            payload["assignees"] = [int(assignee_id)]
        except ValueError:
            payload["assignees"] = [assignee_id]
            
    data = make_request("POST", f"/list/{list_id}/task", payload)
    print(f"Successfully created task '{data.get('name')}' (ID: {data.get('id')})")
    return data

def cmd_create_subtask(list_id: str, parent_task_id: str, title: str, description: str = ""):
    ptid = clean_task_id(parent_task_id)
    payload = {"name": title, "description": description, "parent": ptid}
    data = make_request("POST", f"/list/{list_id}/task", payload)
    print(f"  └─ Subtask created: '{data.get('name')}' (ID: {data.get('id')})")
    return data

def cmd_create_from_doc(doc_filepath: str, list_id: str):
    if not os.path.exists(doc_filepath):
        print(f"Error: File not found at {doc_filepath}", file=sys.stderr)
        sys.exit(1)
        
    with open(doc_filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Extract Title from first H1 header or filename
    title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    parent_title = title_match.group(1).strip() if title_match else os.path.basename(doc_filepath)
    
    print(f"Parsing PRD/FRD Document: {doc_filepath}")
    print(f"Parent Task Title: {parent_title}")
    
    # Create Parent Task
    parent_desc = f"Generated from document: `{os.path.basename(doc_filepath)}`\n\n{content[:1500]}..."
    parent_task = cmd_create_task(list_id, f"[SPEC] {parent_title}", parent_desc)
    parent_id = parent_task.get("id")
    
    # Extract bullet points / checklist items as subtasks
    subtasks = re.findall(r"^(?:- |\* |\d+\. |- \[ \] )(.*[a-zA-Z0-9].*)$", content, re.MULTILINE)
    unique_subtasks = list(dict.fromkeys([s.strip() for s in subtasks if len(s.strip()) > 5]))[:10]
    
    print(f"Creating {len(unique_subtasks)} subtasks from document requirements...")
    for sub_title in unique_subtasks:
        cmd_create_subtask(list_id, parent_id, sub_title, f"Requirement item from {os.path.basename(doc_filepath)}")
        
    print(f"\nSuccessfully generated ClickUp Task Hierarchy for '{parent_title}' (Parent ID: {parent_id})")

def cmd_delete_task(task_id: str):
    tid = clean_task_id(task_id)
    make_request("DELETE", f"/task/{tid}")
    print(f"Successfully deleted task {tid}")

def cmd_update_status(task_id: str, status: str):
    tid = clean_task_id(task_id)
    payload = {"status": status.lower()}
    data = make_request("PUT", f"/task/{tid}", payload)
    print(f"Successfully updated task {tid} status to '{data.get('status', {}).get('status')}'")

def cmd_update_description(task_id: str, description: str):
    tid = clean_task_id(task_id)
    payload = {"description": description}
    make_request("PUT", f"/task/{tid}", payload)
    print(f"Successfully updated description for task {tid}")

def cmd_clear_description(task_id: str):
    tid = clean_task_id(task_id)
    payload = {"description": ""}
    make_request("PUT", f"/task/{tid}", payload)
    print(f"Successfully cleared description for task {tid}")

def cmd_set_priority(task_id: str, priority_str: str):
    tid = clean_task_id(task_id)
    p_val = PRIORITY_MAP.get(priority_str.lower())
    payload = {"priority": p_val}
    make_request("PUT", f"/task/{tid}", payload)
    print(f"Successfully updated priority for task {tid} to '{priority_str}'")

def cmd_assign_user(task_id: str, user_id: str):
    tid = clean_task_id(task_id)
    try:
        uid = int(user_id)
    except ValueError:
        uid = user_id
    payload = {"assignees": {"add": [uid]}}
    make_request("PUT", f"/task/{tid}", payload)
    print(f"Successfully assigned user {user_id} to task {tid}")

def cmd_remove_user(task_id: str, user_id: str):
    tid = clean_task_id(task_id)
    try:
        uid = int(user_id)
    except ValueError:
        uid = user_id
    payload = {"assignees": {"rem": [uid]}}
    make_request("PUT", f"/task/{tid}", payload)
    print(f"Successfully removed user {user_id} from task {tid}")

def cmd_reassign_user(task_id: str, old_user_id: str, new_user_id: str):
    tid = clean_task_id(task_id)
    try:
        old_uid = int(old_user_id)
        new_uid = int(new_user_id)
    except ValueError:
        old_uid, new_uid = old_user_id, new_user_id
    payload = {"assignees": {"rem": [old_uid], "add": [new_uid]}}
    make_request("PUT", f"/task/{tid}", payload)
    print(f"Successfully reassigned task {tid} from user {old_user_id} to user {new_user_id}")

def cmd_add_comment(task_id: str, comment_text: str):
    tid = clean_task_id(task_id)
    payload = {"comment_text": comment_text, "notify_all": False}
    make_request("POST", f"/task/{tid}/comment", payload)
    print(f"Successfully posted comment to ClickUp task {tid}")

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("--help", "-h"):
        print(__doc__)
        sys.exit(0)
        
    cmd = sys.argv[1].lower()
    
    if cmd == "get-workspaces":
        cmd_get_workspaces()
    elif cmd == "get-spaces" and len(sys.argv) >= 3:
        cmd_get_spaces(sys.argv[2])
    elif cmd == "get-lists" and len(sys.argv) >= 3:
        cmd_get_lists(sys.argv[2])
    elif cmd == "create-list" and len(sys.argv) >= 4:
        cmd_create_list(sys.argv[2], sys.argv[3])
    elif cmd == "delete-list" and len(sys.argv) >= 3:
        cmd_delete_list(sys.argv[2])
    elif cmd == "get" and len(sys.argv) >= 3:
        cmd_get_task(sys.argv[2])
    elif cmd == "search-tasks" and len(sys.argv) >= 3:
        q = sys.argv[3] if len(sys.argv) >= 4 else ""
        cmd_search_tasks(sys.argv[2], q)
    elif cmd == "create-task" and len(sys.argv) >= 4:
        desc = sys.argv[4] if len(sys.argv) >= 5 else ""
        prio = sys.argv[5] if len(sys.argv) >= 6 else None
        uid = sys.argv[6] if len(sys.argv) >= 7 else None
        cmd_create_task(sys.argv[2], sys.argv[3], desc, prio, uid)
    elif cmd == "create-subtask" and len(sys.argv) >= 5:
        desc = sys.argv[5] if len(sys.argv) >= 6 else ""
        cmd_create_subtask(sys.argv[2], sys.argv[3], sys.argv[4], desc)
    elif cmd == "create-from-doc" and len(sys.argv) >= 4:
        cmd_create_from_doc(sys.argv[2], sys.argv[3])
    elif cmd == "delete-task" and len(sys.argv) >= 3:
        cmd_delete_task(sys.argv[2])
    elif cmd == "update-status" and len(sys.argv) >= 4:
        cmd_update_status(sys.argv[2], sys.argv[3])
    elif cmd == "update-description" and len(sys.argv) >= 4:
        cmd_update_description(sys.argv[2], sys.argv[3])
    elif cmd == "clear-description" and len(sys.argv) >= 3:
        cmd_clear_description(sys.argv[2])
    elif cmd == "set-priority" and len(sys.argv) >= 4:
        cmd_set_priority(sys.argv[2], sys.argv[3])
    elif cmd == "assign-user" and len(sys.argv) >= 4:
        cmd_assign_user(sys.argv[2], sys.argv[3])
    elif cmd == "remove-user" and len(sys.argv) >= 4:
        cmd_remove_user(sys.argv[2], sys.argv[3])
    elif cmd == "reassign-user" and len(sys.argv) >= 5:
        cmd_reassign_user(sys.argv[2], sys.argv[3], sys.argv[4])
    elif cmd == "add-comment" and len(sys.argv) >= 4:
        cmd_add_comment(sys.argv[2], sys.argv[3])
    else:
        print("Invalid arguments or missing parameters. Use --help for usage instructions.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
