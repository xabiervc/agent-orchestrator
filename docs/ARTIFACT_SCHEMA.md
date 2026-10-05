# Artifact Schema

Every run is stored under `.agent/runs/<run-id>/`.

```text
<run-id>/
├── task.json
├── consensus.json
├── proposals/*.json
├── reviews/*.json
├── prompts/*
└── evidence/*
```

Provider results should include:

```json
{
  "schema_version": 1,
  "type": "provider_result",
  "run_id": "...",
  "provider": "claude-code",
  "role": "planning",
  "status": "completed",
  "model_requested": "sonnet",
  "model_reported": "...",
  "files_changed": [],
  "verification": []
}
```

Never put credentials, tokens, cookies, or private provider configuration into an artifact.
