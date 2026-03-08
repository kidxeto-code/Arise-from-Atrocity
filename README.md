# Ashbound: Escape from Hell

A playable **2D roguelike platformer prototype** where Kael Ashwalker fights through Hell's layers and the Seven Sins to reclaim his soul.

## What's implemented

- **Platformer combat loop** (move, jump, dash, melee attack).
- **Roguelike progression** via waves, random events, scaling encounters, and run-based loot.
- **Lore-connected hierarchy**:
  - Main bosses are the Seven Sins (Wrath, Pride, Envy, Greed, Lust, Gluttony, Sloth).
  - Mini-bosses with unique identities and move lists.
- **Unique move definitions**:
  - Regular enemies have distinct move sets per archetype.
  - Each mini-boss and each sin boss has its own unique move list.
- **Skill tree** supporting different play styles (tank, damage, crit, mobility).
- **Inventory system** with capacity management and item usage.
- **60+ unique items** across rarity tiers, with stat-changing effects.
- **Random events** that alter run state and player build.

## Controls

- `A / D`: Move
- `Space`: Jump (multi-jump from skills)
- `Left Shift`: Dash
- `J`: Attack
- `I`: Use first inventory item
- `U`: Unlock the next available skill (if points allow)

## Run

```bash
python3 -m pip install pygame
python3 main.py
```

## Notes

This is a complete single-run prototype intended as a strong foundation for expansion into a content-heavy production game (save system, room generation, animation, VFX/SFX, UI menus, and authored boss phases).
