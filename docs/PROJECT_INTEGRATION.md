# Project Integration

## Initialize a project

From the consumer repository:

```powershell
agent init --profile godot
```

Replace the generated `.agent/project.json` with project-specific values. The current schema is JSON to keep the first release dependency-free and portable. YAML support may be added after the contract stabilizes.

## Start a run

```powershell
agent start --task "Add a pause menu without changing save data"
```

The command creates `.agent/runs/<run-id>/` with task, proposal, review, prompt, consensus, and evidence directories.

## Provider artifacts

Provider outputs must be JSON files under the run directory. A provider may be unavailable; record the failure rather than inventing output.

## Implementation gate

An implementer may edit only after:

```json
{"decision": "approve"}
```

exists in `consensus.json` and validation passes.
