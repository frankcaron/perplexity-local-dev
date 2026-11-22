"""Perplexity local dev — a simple text-based dungeon crawler.

Run ``python main.py`` to play.  The game is a floor-by-floor crawl: each floor
holds one enemy, you fight it with the ``attack`` command, loot the gold and
XP, and move on.  You can open the ``shop`` any time to buy health potions and
weapon upgrades.  You win by clearing the final floor; you lose when your hit
points reach zero.
"""

from __future__ import annotations

import random
import sys

from rpg import (
    POTION_HEAL,
    POTION_PRICE,
    WEAPON_DAMAGE_GAIN,
    attack,
    buy_potion,
    buy_weapon,
    gain_xp,
    level_stats,
    pick_enemy,
    reward,
    weapon_price,
    xp_reward,
)


def banner() -> None:
    """Print the title block shown when the game starts."""
    print("=" * 40)
    print("  DUNGEON CRAWLER")
    print("  A tiny text-based RPG")
    print("=" * 40)
    print()


def prompt() -> str:
    """Read one command from the player, returning '' on EOF.

    Using a dedicated prompt (instead of relying on ``input``'s echo) keeps
    the CLI testable: tests feed commands through stdin and capture stdout.
    """
    sys.stdout.write("> ")
    sys.stdout.flush()
    line = sys.stdin.readline()
    if not line:  # stdin exhausted (EOF) — end the game gracefully
        return ""
    return line.strip()


def status_line(
    hp: int, max_hp: int, level: int, xp: int,
    weapon_damage: int, gold: int, potions: int,
) -> str:
    """One-line summary of the player's current state."""
    return (
        f"You: level {level}, {xp} XP, {hp}/{max_hp} HP, "
        f"weapon {weapon_damage} dmg, {gold} gold, {potions} potions."
    )


def play_shop(
    hp: int, max_hp: int, weapon_damage: int, gold: int, weapon_upgrades: int,
) -> tuple[int, int, int, int]:
    """Run the shop menu until the player backs out.

    Returns the new ``(hp, gold, weapon_damage, weapon_upgrades)``.  Potions
    are not part of the returned state: buying one applies the heal
    immediately, so no held-potion count is tracked.
    """
    while True:
        print()
        print("Shop goods:")
        print(f"  potion - {POTION_PRICE} gold (heals {POTION_HEAL} HP)")
        print(f"  weapon - {weapon_price(weapon_upgrades)} gold "
              f"(+{WEAPON_DAMAGE_GAIN} damage)")
        print(f"You have {gold} gold.")
        print("Shop: potion, weapon, back")
        choice = prompt().lower()
        if choice in ("", "quit", "back"):
            return hp, gold, weapon_damage, weapon_upgrades
        if choice == "potion":
            result = buy_potion(hp, max_hp, gold)
            if result is None:
                if gold < POTION_PRICE:
                    print("Not enough gold for a potion.")
                else:
                    print("You are already at full HP.")
            else:
                hp, gold = result
                print(f"You drink the potion and feel restored. "
                      f"({hp} HP, {gold} gold left)")
        elif choice == "weapon":
            result = buy_weapon(gold, weapon_upgrades)
            if result is None:
                print("Not enough gold for a weapon upgrade.")
            else:
                gold, weapon_upgrades = result
                weapon_damage += WEAPON_DAMAGE_GAIN
                print(f"You buy a weapon upgrade! "
                      f"({gold} gold left)")
        else:
            print("I don't know that. Try: potion, weapon, back.")


def play(rng: random.Random, final_floor: int = 5) -> None:
    """Run the game loop until the player wins, dies, or quits.

    ``final_floor`` caps the dungeon at five floors by default; tests pass a
    smaller value to keep scripted playthroughs short and deterministic.
    """
    floor = 1
    level = 1
    xp = 0
    max_hp, weapon_damage = level_stats(level)
    hp = max_hp
    gold = 0
    potions = 0
    weapon_upgrades = 0
    enemy_name, enemy_hp = pick_enemy(rng, floor)

    banner()
    print("Commands: attack, status, shop, use potion, quit")
    print()

    while True:
        print(f"Floor {floor} of {final_floor}: a {enemy_name} blocks the way "
              f"({enemy_hp} HP).")
        print(status_line(hp, max_hp, level, xp, weapon_damage, gold, potions))
        print()

        command = prompt().lower()
        if command in ("", "quit"):
            # Both a clean exit (quit) and an exhausted stdin (EOF) end the
            # run gracefully rather than crashing on an empty line.
            print("\nYou leave the dungeon, pocketing your gold. Goodbye!")
            return
        if command == "status":
            print(f"{status_line(hp, max_hp, level, xp, weapon_damage, gold, potions)} "
                  f"The {enemy_name} has {enemy_hp} HP.")
            continue
        if command == "shop":
            hp, gold, weapon_damage, weapon_upgrades = play_shop(
                hp, max_hp, weapon_damage, gold, weapon_upgrades
            )
            continue
        if command == "use potion":
            if potions > 0:
                hp = min(max_hp, hp + POTION_HEAL)
                potions -= 1
                print(f"You drink a potion. ({hp} HP, {potions} left)")
            else:
                print("You have no potions to use.")
            continue
        if command != "attack":
            print("I don't know that command. "
                  "Try: attack, status, shop, use potion, quit.")
            continue

        # One combat round: you strike, then the enemy counters if alive.
        hp, enemy_hp = attack(hp, enemy_hp, weapon_damage, rng)
        if enemy_hp <= 0:
            gold += reward()
            old_level = level
            xp, level = gain_xp(xp, level, xp_reward())
            if level > old_level:
                max_hp, weapon_damage = level_stats(level)
                hp = max_hp  # full heal on level up
                print(f"Level up! You are now level {level} "
                      f"({max_hp} HP, {weapon_damage} weapon damage).")
            print(f"You slay the {enemy_name}! (+{reward()} gold, "
                  f"+{xp_reward()} XP)")
            if floor == final_floor:
                print(f"\nYou have cleared the dungeon at level {level} "
                      f"with {hp} HP and {gold} gold. Victory!")
                return
            floor += 1
            enemy_name, enemy_hp = pick_enemy(rng, floor)
            print(f"You descend to floor {floor}...")
        else:
            print(f"You strike the {enemy_name} for damage; it hits back!")

        if hp <= 0:
            print("\nYou fall on floor "
                  f"{floor}, {gold} gold to the dust. Game over.")
            return


def main() -> None:
    """Entry point: seed the RNG and start the game."""
    rng = random.Random()
    play(rng)


if __name__ == "__main__":
    main()
