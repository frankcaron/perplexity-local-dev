"""Combat and progression rules for the dungeon crawler.

This module is deliberately side-effect-free (except for the RNG it is given):
every function takes the game state as input and returns new values, so the
game loop in ``main.py`` owns all state and the rules stay trivially testable.
"""

from __future__ import annotations

import random

# How much damage a player's attack lands, and how much an enemy counter-lands.
# PLAYER_DAMAGE is the *base* weapon damage; main seeds the player's
# weapon_damage from it and grows it through leveling and shop upgrades.
PLAYER_DAMAGE = 12
ENEMY_DAMAGE = 4

# Enemies that can appear, from weakest to strongest.  Each is a
# (display_name, base_hit_points) pair.  Deep floors reuse the strongest
# entry's name but scale its HP up with the floor (see pick_enemy).
ENEMIES = [
    ("giant rat", 20),
    ("cave bat", 25),
    ("goblin", 35),
    ("skeleton", 45),
    ("dark knight", 60),
]

# Dungeon depth: each run opens a dungeon with a random number of floors,
# drawn uniformly between MIN_FLOOR_COUNT and MAX_FLOOR_COUNT (inclusive).
MIN_FLOOR_COUNT = 5
MAX_FLOOR_COUNT = 50

# Floor difficulty scaling.  Enemy HP rises by ENEMY_HP_FLOOR_STEP for each
# floor above the first, so the climb gets harder; gold and XP rewards rise in
# step so higher floors are also more lucrative.  The player's own power grows
# more gently (FLOOR_HP_GAIN / FLOOR_DAMAGE_GAIN per floor) so each floor is a
# little harder to clear while a full run stays achievable with shop upgrades.
ENEMY_HP_FLOOR_STEP = 10
REWARD_GOLD_FLOOR_STEP = 5
XP_FLOOR_STEP = 10
FLOOR_HP_GAIN = 4
FLOOR_DAMAGE_GAIN = 2

# Gold the player pockets for each enemy defeated, on floor 1.
REWARD_GOLD = 10

# Leveling: each kill grants XP_PER_KILL experience; advancing past the
# threshold costs XP_PER_LEVEL * level, and each new level raises max HP and
# weapon damage.
XP_PER_LEVEL = 20
XP_PER_KILL = 20
LEVEL_HP_GAIN = 10
LEVEL_DAMAGE_GAIN = 3

# Shop catalog: a health potion and a weapon upgrade, with rising weapon prices.
POTION_PRICE = 15
POTION_HEAL = 25
BASE_WEAPON_PRICE = 20
WEAPON_PRICE_STEP = 15
# How much damage each shop weapon upgrade adds, on top of level growth.
WEAPON_DAMAGE_GAIN = 5

# Base hit points for a level-1 player; level_stats grows from here.
BASE_MAX_HP = 50


def random_floor_count(rng: random.Random) -> int:
    """Draw the dungeon depth for a new run.

    Returns a uniformly random integer between MIN_FLOOR_COUNT and
    MAX_FLOOR_COUNT (inclusive) using the given ``rng``.
    """
    return rng.randint(MIN_FLOOR_COUNT, MAX_FLOOR_COUNT)


def pick_enemy(rng: random.Random, floor: int) -> tuple[str, int]:
    """Choose an enemy for ``floor``.

    The name is clamped to the last entry in the enemy table, so deep floors
    reuse the strongest foe (no cycling or re-spawns).  The enemy's HP is that
    entry's base plus ``ENEMY_HP_FLOOR_STEP`` for each floor above the first, so
    the climb gets harder: the floor-1 giant rat stays at 20 HP, while a floor-50
    dark knight reaches 60 + 10 * 49 = 550 HP.  ``rng`` is reserved for future
    randomness and currently unused.
    """
    name, base_hp = ENEMIES[min(floor - 1, len(ENEMIES) - 1)]
    return name, base_hp + ENEMY_HP_FLOOR_STEP * (floor - 1)


def attack(
    player_hp: int, enemy_hp: int, weapon_damage: int, rng: random.Random
) -> tuple[int, int]:
    """Resolve one round: player hits first, then the enemy counters if alive.

    Returns the new ``(player_hp, enemy_hp)`` pair, each clamped at zero.
    ``rng`` is reserved for future randomness and currently unused.
    """
    enemy_hp -= weapon_damage
    if enemy_hp > 0:
        player_hp -= ENEMY_DAMAGE
    return max(0, player_hp), max(0, enemy_hp)


def reward(floor: int) -> int:
    """Gold awarded for a victory on ``floor``.

    Rises by ``REWARD_GOLD_FLOOR_STEP`` for each floor above the first, so
    higher floors pay more.  Floor 1 returns the base ``REWARD_GOLD``.
    """
    return REWARD_GOLD + REWARD_GOLD_FLOOR_STEP * (floor - 1)


def xp_reward(floor: int) -> int:
    """Experience awarded for a victory on ``floor``.

    Rises by ``XP_FLOOR_STEP`` for each floor above the first, so higher floors
    grant more XP.  Floor 1 returns the base ``XP_PER_KILL``.
    """
    return XP_PER_KILL + XP_FLOOR_STEP * (floor - 1)


def xp_to_next(level: int) -> int:
    """Experience needed to advance from ``level`` to the next one.

    A linear curve: each level costs a bit more than the last.
    """
    return XP_PER_LEVEL * level


def gain_xp(xp: int, level: int, gained: int) -> tuple[int, int]:
    """Award ``gained`` XP, applying any number of level ups.

    Returns the new ``(xp, level)`` pair, with xp kept below the next
    threshold after each advance.
    """
    new_xp = xp + gained
    new_level = level
    while new_xp >= xp_to_next(new_level):
        new_xp -= xp_to_next(new_level)
        new_level += 1
    return new_xp, new_level


def level_stats(level: int) -> tuple[int, int]:
    """Return ``(max_hp, weapon_damage)`` for a given level.

    Base stats are (BASE_MAX_HP, PLAYER_DAMAGE); each level above 1 adds
    LEVEL_HP_GAIN max HP and LEVEL_DAMAGE_GAIN weapon damage.
    """
    bonus = level - 1
    return (
        BASE_MAX_HP + LEVEL_HP_GAIN * bonus,
        PLAYER_DAMAGE + LEVEL_DAMAGE_GAIN * bonus,
    )


def floor_bonus_stats(floor: int) -> tuple[int, int]:
    """Return the ``(extra_max_hp, extra_weapon_damage)`` a floor grants.

    Grows linearly with depth: ``FLOOR_HP_GAIN`` extra max HP and
    ``FLOOR_DAMAGE_GAIN`` extra weapon damage for each floor above the first.
    Floor 1 returns ``(0, 0)``.  The game loop adds this on top of the
    level-based stats so the player grows a little with the climb.
    """
    bonus = floor - 1
    return FLOOR_HP_GAIN * bonus, FLOOR_DAMAGE_GAIN * bonus


def weapon_damage(level: int, upgrades: int) -> int:
    """Total weapon damage for a player at ``level`` with ``upgrades``.

    Combines the level-based damage growth with the flat bonus from each
    shop weapon upgrade, so upgrades persist across level-ups.
    """
    return level_stats(level)[1] + WEAPON_DAMAGE_GAIN * upgrades


def weapon_price(upgrades: int) -> int:
    """Price of the next weapon upgrade; each purchase raises the cost."""
    return BASE_WEAPON_PRICE + WEAPON_PRICE_STEP * upgrades


def buy_potion(gold: int) -> int | None:
    """Buy a health potion for POTION_PRICE.

    Returns the remaining gold after the purchase, or ``None`` if the
    player cannot afford it.  No HP logic: buying no longer heals.
    """
    if gold < POTION_PRICE:
        return None
    return gold - POTION_PRICE


def use_potion(hp: int, max_hp: int, potions: int) -> tuple[int, int] | None:
    """Drink a held potion: heal POTION_HEAL HP (capped at max) and decrement.

    Returns ``(new_hp, new_potions)`` on success, or ``None`` if the player
    has no potions or is already at full HP (do not waste a potion).
    """
    if potions <= 0 or hp >= max_hp:
        return None
    return min(max_hp, hp + POTION_HEAL), potions - 1


def buy_weapon(gold: int, upgrades: int) -> tuple[int, int] | None:
    """Buy a weapon upgrade for its current price.

    Returns ``(new_gold, new_upgrades)`` on success, or ``None`` if the
    player cannot afford the next upgrade.
    """
    price = weapon_price(upgrades)
    if gold < price:
        return None
    return gold - price, upgrades + 1
