# Sample ClickUp Workflow Transcripts

This transcript demonstrates an agent executing ClickUp task workflows using **MCP Tooling** (Scenario 1), **REST API Helper** (Scenario 2), and **PRD/FRD Document Task Generation** (Scenario 3).

---

## Scenario 1: Priority 1 — Native MCP Integration

**User**:  
> Work on ClickUp task `CU-8675309`. Fetch the ticket details and implement what is requested.

**Agent** *(Detects active ClickUp MCP server)*:  
> Invoking MCP tool `clickup_get_task` with `{ "taskId": "CU-8675309" }`...

---

## Scenario 2: Priority 2 — REST API Fallback (`CLICKUP_API_TOKEN`)

**Agent**:  
> ClickUp MCP server is not active. Falling back to REST API helper script (`scripts/clickup_helper.py`)...
> 
> 1. `python3 .agents/skills/clickup/scripts/clickup_helper.py get CU-8675309`
> 2. `python3 .agents/skills/clickup/scripts/clickup_helper.py update-status CU-8675309 "in progress"`

---

## Scenario 3: Creating ClickUp Tasks from PRD / FRD Document

**User**:  
> Please create ClickUp tasks for our new Real-Time Notifications feature from the PRD document.

**Agent**:  
1. **Searching for Document** (3-Step Search Strategy):
   - Checking `docs/` folder... Found `docs/PRD_realtime_notifications.md`!
2. **Parsing Document**:
   - Title: *Real-Time Event Delivery Engine (SSE + Redis Pub/Sub)*
   - Requirements extracted: 4 core subtasks.
3. **Generating Task Hierarchy**:
   - Creating Parent Task: `[SPEC] Real-Time Event Delivery Engine` (ID: `CU-9900112`)
   - Creating Subtask 1: `Implement GET /api/v1/notifications/stream SSE endpoint`
   - Creating Subtask 2: `Setup Redis Pub/Sub listener on Node API instances`
   - Creating Subtask 3: `Add PostgreSQL user_notifications DDL & unread index`
   - Creating Subtask 4: `Implement client exponential backoff reconnect handler`

**Summary Output**:
> Successfully created ClickUp Task Hierarchy under List `123456`:
> - **Parent Task**: `[SPEC] Real-Time Event Delivery Engine` (ID: `CU-9900112`)
> - **Subtasks**: 4 requirement items linked under Parent Task `CU-9900112`.
