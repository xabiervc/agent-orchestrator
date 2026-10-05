# Architecture

## Principles

1. The consumer repository owns project truth.
2. The orchestrator owns protocol, routing, schemas, and validation.
3. Providers are replaceable.
4. Run artifacts are explicit and inspectable.
5. One approved implementer edits a task.
6. Missing providers never become approval.
7. Credentials never enter artifacts.

## Layers

```text
core protocol
  ├── configuration
  ├── run lifecycle
  ├── routing
  ├── provider command plans
  ├── deterministic consensus
  └── validation

profiles
  ├── generic
  ├── Godot
  ├── Unreal
  ├── Unity
  ├── mobile
  ├── web
  ├── desktop
  └── backend
```

The core does not depend on an engine, UI, or model vendor.
