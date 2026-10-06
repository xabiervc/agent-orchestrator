# Game Event Contract

Gameplay systems communicate with audio, animation, UI, and presentation through named events.

Example events:

```text
player.spawned
player.jump
player.land
player.attack_started
player.attack_hit
player.damage
enemy.alerted
enemy.died
item.collected
combat.started
combat.ended
game.won
game.lost
scene.loading
scene.loaded
menu.opened
menu.closed
```

Each response declares a channel and action. The orchestrator validates names and uniqueness but does not execute engine code.
