# Run Lifecycle

Runs move through explicit states:

```text
created -> planning -> reviewing -> consensus -> approved -> implementing -> verifying -> completed
```

Use `agent transition --to <state>` to persist a valid transition. A run may become `blocked` or `failed`, and can return to planning according to the state machine.

A handoff requires approved consensus and writes a scope-locked `handoff.json`.
