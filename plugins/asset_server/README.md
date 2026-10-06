# Asset Server Plugin

Optional integration boundary for `3d-asset-server` and compatible HTTP/MCP asset services.

The plugin is intentionally transport-agnostic. The core receives injected search and download transports, so unit tests do not access the network.

## Safety contract

- Search does not download assets.
- Downloads require `approved=True`.
- Only public HTTP(S) URLs are accepted.
- Private, loopback, and localhost destinations are rejected.
- Destinations must remain under the configured asset root.
- Existing files are protected unless overwrite is explicitly allowed by both request and policy.
- Unknown or disallowed licenses are rejected by default.
- ZIP traversal is rejected.
- Downloaded files are never executed.
- Every successful download returns provenance and a SHA-256 hash.
