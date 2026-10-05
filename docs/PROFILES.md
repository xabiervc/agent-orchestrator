# Project Profiles

Profiles describe capabilities and risk areas without coupling the core to a specific engine or platform.

A consumer project may combine profiles, for example:

```json
{"profiles": ["unreal", "desktop"]}
```

or:

```json
{"profiles": ["web", "backend"]}
```

Engine and platform integrations should be optional plugins. The core should remain installable without Godot, Unreal, Unity, Android Studio, Xcode, or browser tooling.
