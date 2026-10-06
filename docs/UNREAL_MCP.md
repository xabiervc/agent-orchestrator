# Unreal MCP Integration

Unreal Engine 5.8 includes an experimental MCP server. The official Epic plugin for Claude Code provides skills for using the editor MCP toolsets. This repository treats both as optional external dependencies.

## Project setup

In the Unreal Editor, enable the relevant MCP server and toolset plugins, restart the editor, start the local server, and generate the client configuration for Claude Code. Keep the server bound to localhost and start Claude Code from the folder containing the `.uproject` file.

The orchestrator does not perform these setup actions. It validates the resulting `.uproject` and `.mcp.json`, generates a read-only probe, and blocks write handoffs until the preflight is ready.

## Safe workflow

```text
commit
  -> preflight
  -> read-only probe
  -> one-system proposal
  -> consensus
  -> approved handoff
  -> compile
  -> screenshot and log review
  -> manual playtest
  -> commit
```

Stop the game before editor changes. Do not make changes during C++ or shader compilation. Keep MCP local because the server has no authentication boundary suitable for exposure to a network.
