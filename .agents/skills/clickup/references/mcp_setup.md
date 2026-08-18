# Setting Up ClickUp MCP Server Across AI Coding Agents

Model Context Protocol (MCP) allows any compliant AI coding agent (Claude Code, Antigravity, Gemini CLI, Cursor, Windsurf, etc.) to natively invoke ClickUp tools without requiring custom cURL scripts or API token management in code.

---

## Standard MCP Configuration (`mcp_config.json` or `.agents/mcp_config.json`)

To connect ClickUp via MCP, add the ClickUp MCP server entry to your project's `.agents/mcp_config.json` or your global MCP settings file:

```json
{
  "mcpServers": {
    "clickup": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-clickup"
      ],
      "env": {
        "CLICKUP_API_TOKEN": "pk_YOUR_CLICKUP_PERSONAL_API_TOKEN"
      }
    }
  }
}
```

---

## Agent-Specific Setup Examples

### 1. Antigravity & Gemini CLI
Add the snippet above into `.agents/mcp_config.json` at the root of your repository or into `~/.gemini/config/mcp_config.json`.

### 2. Claude Code & Claude Desktop
- **Claude Code CLI**: Run `claude mcp add clickup npx -y @modelcontextprotocol/server-clickup --env CLICKUP_API_TOKEN=pk_YOUR_TOKEN`
- **Claude Desktop**: Add the JSON block to `~/Library/Application Support/Claude/claude_desktop_config.json`.

### 3. Cursor / Windsurf
Add to `.cursor/mcp.json` or Cursor Settings -> Features -> MCP Servers.

---

## Native MCP Tools Exposed by ClickUp Server

When active, the following native tools become available to the agent automatically:
- `clickup_get_task`
- `clickup_update_task`
- `clickup_create_task`
- `clickup_create_comment`
- `clickup_list_tasks`

---

## Fallback Mechanism
If the agent detects that the MCP tools above are not loaded (e.g. MCP server failed to start or token is missing), it will automatically degrade to using the CLI script fallback:
```bash
python3 .agents/skills/clickup/scripts/clickup_helper.py get <task_id>
```
