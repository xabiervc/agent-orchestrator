# Visual Pipeline

The visual pipeline combines optional asset search, Blender, and an engine integration.

```text
asset server -> Blender -> asset validator -> Godot or Unreal -> runtime evidence
```

## Asset contract

A visual asset should define:

- type and target engine;
- export format and destination;
- scale units and origin;
- triangle budget;
- material-slot budget;
- required animation actions;
- license and provenance when derived from external assets.

## Character workflow

```text
silhouette -> base mesh -> clothing -> UV -> materials -> armature -> weights -> idle -> locomotion -> combat -> export -> engine import -> runtime check
```

Do not treat a generated character as complete until scale, materials, skeleton, animations, and in-engine behavior have been verified.
