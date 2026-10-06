# Godot MCP Integration

Godot does not ship a single official MCP server equivalent to Unreal Engine 5.8. This repository therefore provides an adapter boundary for compatible Godot MCP servers and editor addons.

## Supported configuration shapes

The validator accepts declarative stdio configurations and local HTTP/WebSocket configurations. It does not install an addon or connect to a server.

## Safe workflow

```text
commit
  -> preflight
  -> read-only probe
  -> one-system proposal
  -> consensus
  -> approved handoff
  -> project checks
  -> run and inspect debugger output
  -> manual playtest
  -> commit
```

Keep live-editor integrations local. Prefer stdio when available because it does not expose a listening network port. Use local WebSocket or HTTP only when the selected Godot integration requires it.

## High-risk areas

Treat project settings, autoloads, input actions, save data, resource UIDs, export presets, and plugin installation as high-risk. Require explicit approval and a fresh verification pass for those changes.
