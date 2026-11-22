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
    use_potion,
    weapon_damage,
    weapon_price,
    xp_reward,
)


def rpg_weapon_damage(level: int, upgrades: int) -> int:
    """Total weapon damage: level growth + shop upgrades."""
    return weapon_damage(level, upgrades)


def banner() -> None:
    """Print the title block shown when the game starts."""
    print("=" * 40)
    print("  DUNGEON CRAWLER")
    print("  A tiny text-based RPG")
    print("=" * 40)
    print()


def prompt() -> str | None:
    """Read one command from the player.

    Returns ``None`` on EOF (stdin exhausted) and the stripped line otherwise
    (a blank line returns ``""``).  Using a dedicated prompt (instead of
    relying on ``input``'s echo) keeps the CLI testable: tests feed commands
    through stdin and capture stdout.
    """
    sys.stdout.write("> ")
    sys.stdout.flush()
    line = sys.stdin.readline()
    if not line:  # stdin exhausted (EOF)
        return None
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
    gold: int, weapon_upgrades: int, potions: int,
) -> tuple[int, int, int]:
    """Run the shop menu until the player backs out or quits.

    Returns the new ``(gold, weapon_upgrades, potions)``.  Potions are held
    items: buying one increments the count; the player drinks them with
    ``use potion`` outside the shop.
    """
    while True:
        print()
        print("Shop goods:")
        print(f"  potion - {POTION_PRICE} gold (heals {POTION_HEAL} HP)")
        print(f"  weapon - {weapon_price(weapon_upgrades)} gold "
              f"(+{WEAPON_DAMAGE_GAIN} damage)")
        print(f"You have {gold} gold.")
        print("Shop: potion, weapon, back")
        choice = prompt()
        if choice is None or choice.lower() in ("quit", "back"):
            return gold, weapon_upgrades, potions
        choice = choice.lower()
        if choice == "":
            print("I don't know that. Try: potion, weapon, back.")
            continue
        if choice == "potion":
            result = buy_potion(gold)
            if result is None:
                print("Not enough gold for a potion.")
            else:
                gold = result
                potions += 1
                print(f"You buy a potion. "
                      f"({gold} gold left, {potions} potions)")
        elif choice == "weapon":
            result = buy_weapon(gold, weapon_upgrades)
            if result is None:
                print("Not enough gold for a weapon upgrade.")
            else:
                gold, weapon_upgrades = result
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
    max_hp, _ = level_stats(level)
    hp = max_hp
    gold = 0
    potions = 0
    weapon_upgrades = 0
    enemy_name, enemy_hp = pick_enemy(rng, floor)

    banner()
    print("Commands: attack, status, shop, use potion, quit")
    print()

    while True:
        weapon_damage = rpg_weapon_damage(level, weapon_upgrades)
        print(f"Floor {floor} of {final_floor}: a {enemy_name} blocks the way "
              f"({enemy_hp} HP).")
        print(status_line(hp, max_hp, level, xp, weapon_damage, gold, potions))
        print()

        command = prompt()
        if command is None or command.lower() == "quit":
            print("\nYou leave the dungeon, pocketing your gold. Goodbye!")
            return
        command = command.lower()
        if command == "":
            print("Type a command: attack, status, shop, use potion, quit.")
            continue
        if command == "status":
            print(f"{status_line(hp, max_hp, level, xp, weapon_damage, gold, potions)} "
                  f"The {enemy_name} has {enemy_hp} HP.")
            continue
        if command == "shop":
            gold, weapon_upgrades, potions = play_shop(
                gold, weapon_upgrades, potions
            )
            continue
        if command == "use potion":
            result = use_potion(hp, max_hp, potions)
            if result is None:
                if potions == 0:
                    print("You have no potions to use.")
                else:
                    print("You are already at full HP.")
            else:
                hp, potions = result
                print(f"You drink a potion. ({hp} HP, {potions} left)")
            continue
        if command != "attack":
            print("I don't know that command. "
                  "Try: attack, status, shop, use potion, quit.")
            continue

        # One combat round: you strike, then the enemy counters if alive.
        hp_before = hp
        enemy_before = enemy_hp
        hp, enemy_hp = attack(hp, enemy_hp, weapon_damage, rng)
        if enemy_hp <= 0:
            gold_gain = reward()
            xp_gain = xp_reward()
            gold += gold_gain
            old_level = level
            xp, level = gain_xp(xp, level, xp_gain)
            if level > old_level:
                max_hp, _ = level_stats(level)
                hp = max_hp  # full heal on level up
                new_dmg = rpg_weapon_damage(level, weapon_upgrades)
                print(f"Level up! You are now level {level} "
                      f"({max_hp} HP, {new_dmg} weapon damage).")
            print(f"You slay the {enemy_name}! (+{gold_gain} gold, "
                  f"+{xp_gain} XP)")
            if floor == final_floor:
                print(f"\nYou have cleared the dungeon at level {level} "
                      f"with {hp} HP and {gold} gold. Victory!")
                return
            floor += 1
            enemy_name, enemy_hp = pick_enemy(rng, floor)
            print(f"You descend to floor {floor}...")
        else:
            dealt = enemy_before - enemy_hp
            taken = hp_before - hp
            print(f"You strike the {enemy_name} for {dealt} damage; "
                  f"it hits back for {taken}.")

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
