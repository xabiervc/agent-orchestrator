# agent-orchestrator

A deterministic, evidence-oriented orchestration core for software and game-production workflows.

## Install

```bash
python -m pip install -e .
```

For development:

```bash
python -m pip install -r requirements-dev.txt
```

## Quickstart

```bash
agent init --profile generic
agent start --task "Release smoke test"
agent transition --to planning
agent transition --to reviewing
agent transition --to consensus
agent quality --command 'tests=python -c "print(1)"'
```

The CLI returns exit code `0` when required quality gates pass and `1` otherwise.

## Lifecycle

Runs are stored under `.agent/runs/<run-id>/`:

- `run.json`: compatibility manifest with task, state and history.
- `state.json`: current persisted state.
- `proposals/`: planner proposals.
- `reviews/`: reviewer outputs.
- `evidence/manifest.json`: command evidence and hashes.

Valid lifecycle states are `created`, `planning`, `reviewing`, `consensus`, `advanced`, `completed` and `failed`. Invalid transitions are rejected.

## Quality gates

Use `--result NAME=true|false` for precomputed results or `--command NAME=COMMAND` for safe execution. Commands are tokenized and executed without a shell, with timeouts and project-root directory validation.

## Development

```bash
pytest -q
ruff check .
mypy agent_orchestrator
pytest --cov=agent_orchestrator --cov-report=term-missing
```

See [the quickstart](examples/quickstart/README.md) and [release notes](RELEASE_NOTES_v0.1.1.md).
