# Unreal MCP Plugin

Optional local-only integration boundary for the Unreal Engine MCP server and the official Unreal Engine skills for Claude Code.

## Safety contract

- The plugin does not install Unreal or modify `.uproject` files.
- The core does not open MCP connections.
- `.mcp.json` must use HTTP(S) and resolve to localhost or a private local address.
- A read-only probe is required before a write handoff.
- Play mode and active compilation block write work.
- Use source control before every live-editor session.
- Keep permissions enabled; never use dangerous permission bypasses with live editor access.

The plugin produces diagnostics and prompts. An external operator or provider is responsible for executing them.
