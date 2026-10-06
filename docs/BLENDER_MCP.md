# Blender MCP Integration

This plugin provides a provider-neutral boundary for Blender MCP servers. It supports declarative stdio and local HTTP/WebSocket configuration validation, but it does not install or run Blender.

## Safe workflow

```text
commit or save checkpoint
  -> preflight
  -> read-only probe
  -> visual task proposal
  -> consensus
  -> approved Blender handoff
  -> preview render
  -> asset contract validation
  -> explicit export
  -> engine import
  -> runtime verification
```

## Visual task routing

Use Haiku for inspection and metadata, Sonnet for simple props and materials, and Opus for characters, rigging, animation, procedural geometry, and difficult visual debugging. Keep effort at medium unless a specific task justifies escalation.

Never expose a local Blender MCP endpoint to the network. Treat Python execution as arbitrary code execution.
