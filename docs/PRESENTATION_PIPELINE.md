# Presentation Pipeline

Presentation contracts describe scene fades, camera blends, audio crossfades, input locking, screen shake, hit feedback, slow motion, and loading transitions.

Every transition must release input and complete its audio and camera work. Runtime evidence should check that no black screen, duplicate music, stuck input lock, or lingering effect remains.
