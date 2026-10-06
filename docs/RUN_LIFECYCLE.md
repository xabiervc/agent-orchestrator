# Run Lifecycle

Runs move through explicit states:

```text
created -> planning -> reviewing -> consensus -> approved -> implementing -> verifying -> completed
```

A run may become `blocked` or `failed`. Implementers must not edit during `created`, `planning`, `reviewing`, `consensus`, `blocked`, or `failed` states.

Transitions are deterministic and invalid jumps are rejected.
