# Asset Pipeline

The asset server is an optional plugin, not part of the provider-agnostic core.

## Flow

```text
agent task
  -> asset search
  -> license and format review
  -> consensus approval
  -> explicit download
  -> archive and destination validation
  -> provenance artifact
  -> engine import and verification
```

A project enables the capability with an `asset-pipeline` profile. The plugin can connect to `3d-asset-server` through an injected HTTP or MCP transport. The repository does not install or run that server automatically.

Required provenance fields include provider, source URL, license, attribution requirement, destination, SHA-256, and download timestamp.
