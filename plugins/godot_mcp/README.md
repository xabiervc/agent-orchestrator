# Godot MCP Plugin

Optional integration boundary for Godot MCP servers and editor addons. The core does not choose or install a specific community server.

## Safety contract

- The plugin does not install Godot or modify project files.
- The core does not open MCP connections.
- stdio, local HTTP, and local WebSocket configurations can be validated.
- Network MCP endpoints are rejected by default.
- A read-only probe is required before a write handoff.
- Game execution and asset importing block write work.
- Project settings, autoloads, input actions, save data, UIDs, export presets, and plugin installation are high-risk operations.
- Provider execution remains external.
