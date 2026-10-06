# CLI Workflow

```text
agent init --profile godot
agent start --task "Add a pause menu"
agent transition --to planning
agent transition --to reviewing
agent transition --to consensus
agent consensus
agent transition --to approved
agent handoff --provider claude-code --model sonnet --allowed-file player.gd --verify-command "godot --headless --editor --quit"
agent transition --to implementing
agent transition --to verifying
agent evidence --entry path=screenshot.png,kind=screenshot
agent quality --result tests=true --result validation=true --result evidence=true
agent transition --to completed
```

The CLI prepares and validates artifacts. It does not execute providers or project commands.
