# Video explainer profile (design notes)

Status: proposal only. Nothing in this document is implemented yet, and no code, test or CI behaviour depends on it.

These notes distil ideas from an external prompt for producing short explainer films. They are written in our own words and describe what a future profile could enforce.

## Goal

Turn a topic into a finished, rendered explainer video (with sound and captions) that leaves a stated audience with one new understanding. A plan, a moodboard or a single still frame is not a deliverable.

## Inputs

- Topic.
- Audience and what they already believe.
- The outcome expected after watching.
- Target length in seconds.
- Output formats (for example 16:9 master plus 9:16 and 1:1 cuts).
- Brand and reference folders.

## Workflow

1. State the one idea and the viewer outcome in a single sentence.
2. Define design tokens (palette, type, spacing) from the project brand before drawing anything.
3. Compare several visual directions side by side and record the choice and reason.
4. Storyboard as a contact sheet.
5. Animate and fix timing.
6. Full build.
7. Sound and captions.
8. Verification.
9. Export.

## Story shape

Open with a question shown as an image, build the smallest correct model of the idea, prove it on a real case, change one variable to show the turn, and finish by revisiting the opening image with the new understanding plus one next step.

## Verification gates (candidate checks)

- Rendering the same frame twice produces identical output.
- A still is captured at every beat and every line is readable at a small phone width.
- The video is watched muted and the audio is checked on its own.
- Every number shown has an entry in SOURCES.md, otherwise it is removed.
- Contrast, caption and flashing limits are met, and a reduced-motion cut keeps the same sequence of ideas.
- Loudness and peak levels are measured, not assumed.
- Each fix is recorded with before and after evidence.

## Deterministic render contract

- Each frame is a pure function of time.
- A single timeline object holds every beat, move and cue.
- Any randomness is seeded.

## Delivery

Master video, vertical and square cuts, captions, source files and a README that lists only what was actually tested. Partial, failed and untested items are marked as such.

## Autonomy

Creative decisions are made without asking for approval and logged. Stop only for missing rights, unsafe content, or an ambiguity that changes the goal.

## Out of scope for now

- Any implementation, profile file or gate code.
- Attribution claims about the original author's views; the source prompt states it is not written or endorsed by the person it cites.
