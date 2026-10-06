# Release notes v0.1.1

## Included

- Stable CLI lifecycle: `init`, `start`, `transition`, `advance` and `quality`.
- Safe command execution with tokenization, timeout and `shell=False`.
- Persisted `run.json` and `state.json` manifests.
- Proposal, review and evidence directories per run.
- Compatibility APIs for quality, lifecycle, runs and artifacts.
- End-to-end regression coverage.
- CI matrix for Python 3.10, 3.11 and 3.12 with tests, coverage, Ruff, mypy and secret scanning.

## Compatibility

The release preserves result-based quality evaluation and supports both legacy and command-backed gates.
