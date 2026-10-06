# Quickstart

From the repository root:

```bash
python -m pip install -e .
agent init --profile generic
agent start --task "Build a verified feature"
agent transition --to planning
agent transition --to reviewing
agent transition --to consensus
agent quality --command 'tests=python -c "print(1)"'
```

Inspect `.agent/runs/` to review `run.json`, `state.json`, proposals, reviews and evidence.
