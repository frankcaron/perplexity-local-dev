"""Combat resolution for the dungeon crawler.

This module is deliberately side-effect-free (except for the RNG it is given):
every function takes the game state as input and returns new values, so the
game loop in ``main.py`` owns all state and the rules stay trivially testable.
"""

from __future__ import annotations

import random

# How much damage a player's attack lands, and how much an enemy counter-lands.
PLAYER_DAMAGE = 12
ENEMY_DAMAGE = 4

# Enemies that can appear, from weakest to strongest.  Each is a
# (display_name, max_hit_points) pair.
ENEMIES = [
    ("giant rat", 20),
    ("cave bat", 25),
    ("goblin", 35),
    ("skeleton", 45),
    ("dark knight", 60),
]

# Gold the player pockets for each enemy defeated.
REWARD_GOLD = 10


def pick_enemy(rng: random.Random, floor: int) -> tuple[str, int]:
    """Choose an enemy for ``floor``.

    The index is clamped to the enemy table, so early floors get weak foes
    and deep floors cycle through the strongest ones (plus a few re-spawns).
    """
    name, max_hp = ENEMIES[min(floor - 1, len(ENEMIES) - 1)]
    return name, max_hp


def attack(player_hp: int, enemy_hp: int, rng: random.Random) -> tuple[int, int]:
    """Resolve one round: player hits first, then the enemy counters if alive.

    Returns the new ``(player_hp, enemy_hp)`` pair, each clamped at zero.
    """
    enemy_hp -= PLAYER_DAMAGE
    if enemy_hp > 0:
        player_hp -= ENEMY_DAMAGE
    return max(0, player_hp), max(0, enemy_hp)


def reward() -> int:
    """Gold awarded for a single victory."""
    return REWARD_GOLD
