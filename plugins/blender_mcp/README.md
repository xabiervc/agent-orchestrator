# Blender MCP Plugin

Optional local integration boundary for Blender MCP servers and Blender editor addons.

## Visual skills

- `modeling`
- `characters`
- `rigging`
- `animation`
- `materials`
- `environment`
- `export`

Only the selected skill should be loaded for a task. The plugin does not install Blender or a specific MCP server.

## Safety contract

- The core does not open MCP connections.
- Remote MCP endpoints are rejected by default.
- A saved `.blend` file and read-only probe are required before write work.
- Python execution and external commands are blocked by default.
- Destructive edits, overwrites, and exports require explicit approval.
- Source assets are never overwritten by default.
- Provider execution remains external.
