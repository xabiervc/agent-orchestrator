# Agent Orchestrator

Provider-agnostic orchestration core for coding agents across games, apps, web, mobile, and desktop projects.

The project keeps the reusable protocol in one repository and stores project-specific configuration and run artifacts in each consumer repository.

## Design

```text
project repository
  .agent/project.yaml
  .agent/runs/<run-id>/
          |
          v
agent-orchestrator
  routing -> providers -> artifacts -> consensus -> validation
```

The core does not store credentials, install provider CLIs, modify repositories, or execute agents automatically. It creates explicit artifacts and safe command plans for an operator or an external runner.

## Requirements

- Python 3.11+
- Git

## Install

```powershell
python -m pip install -e .
```

## CLI

```powershell
agent init --profile generic
agent start --task "Describe the task"
agent status
agent consensus
agent validate
```

Use `agent --help` for all options.

## Profiles

Profiles describe project capabilities, commands, and risk areas. The initial profiles are:

- `generic`
- `godot`
- `unreal`
- `unity`
- `mobile`
- `web`
- `desktop`
- `backend`

A project may combine profiles in `.agent/project.yaml`.

## Provider policy

The routing defaults are intentionally conservative:

- `haiku`: exploration and mechanical checks;
- `sonnet`: normal planning, implementation, and review;
- `opus`: architecture, persistence, migrations, and hard debugging;
- `fable`: manual opt-in only.

Provider adapters produce command plans. They never embed credentials or assume that a provider is available.

## Repository contract

The consumer repository remains the authority for project design and implementation. Every run is isolated under `.agent/runs/<run-id>/`. Implementers must not edit unless `consensus.json` contains `decision: approve`.

See `docs/ARCHITECTURE.md` and `docs/PROJECT_INTEGRATION.md`.
