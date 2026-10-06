# Agent Orchestrator

Provider-agnostic orchestration core for coding agents and game-production workflows.

## Installation

```bash
python -m pip install -e .
```

## Project setup

Initialize a project with a JSON configuration:

```bash
agent init --profile generic
```

This creates `project.json`. Start a run with:

```bash
agent start --task "Describe the implementation task"
```

## CLI lifecycle

```text
agent init       Create project.json
agent start      Create a run
agent route      Select a provider/model for role and risk
agent provider   Inspect a provider adapter
agent transition Advance the current run state
agent handoff    Write a provider handoff contract
agent quality    Evaluate declared quality gates
agent evidence   Write and validate evidence entries
agent status     Show the current task
agent consensus  Calculate consensus from run artifacts
agent validate   Validate the run artifacts
```

Example routing query:

```bash
agent route --role implementation --risk high
```

Example quality evaluation:

```bash
agent quality \
  --result tests=true \
  --result validation=true \
  --result evidence=true
```

In v0.1, quality results are declared inputs. They are not yet connected automatically to project commands or persisted execution evidence. That is planned for a later release.

## Run artifacts

Runs are stored under `.agent/runs/<run-id>/`. The lifecycle records task, proposals, reviews, prompts, evidence, consensus, and run state as JSON artifacts.

Consensus accepts only valid, completed artifacts with an explicit approval verdict. Missing or non-approval verdicts are not treated as approvals.

## Optional integrations

The repository includes optional, offline-tested adapters and contracts for providers, Godot, Unreal, Blender, 3D assets, and game production. These integrations are not required by the core package and may require separate tools, credentials, APIs, or project-specific validation.

## Development

```bash
pytest -q
```

The graph-based execution engine, command-backed quality gates, and provider authentication checks remain separate follow-up work.