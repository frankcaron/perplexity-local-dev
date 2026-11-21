"""Perplexity local dev — a simple text-based dungeon crawler.

Run ``python main.py`` to play.  The game is a floor-by-floor crawl: each floor
holds one enemy, you fight it with the ``attack`` command, loot the gold, and
move on.  You win by clearing the final floor; you lose when your hit points
reach zero.
"""

from __future__ import annotations

import random
import sys

from rpg import pick_enemy, attack, reward


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


def play(rng: random.Random, final_floor: int = 5) -> None:
    """Run the game loop until the player wins, dies, or quits.

    ``final_floor`` caps the dungeon at five floors by default; tests pass a
    smaller value to keep scripted playthroughs short and deterministic.
    """
    floor = 1
    hp = 50
    gold = 0
    enemy_name, enemy_hp = pick_enemy(rng, floor)

    banner()
    print("Commands: attack, status, quit")
    print()

    while True:
        print(f"Floor {floor} of {final_floor}: a {enemy_name} blocks the way "
              f"({enemy_hp} HP).")
        print(f"You: {hp} HP, {gold} gold.")
        print()

        command = prompt().lower()
        if command in ("", "quit"):
            # Both a clean exit (quit) and an exhausted stdin (EOF) end the
            # run gracefully rather than crashing on an empty line.
            print("\nYou leave the dungeon, pocketing your gold. Goodbye!")
            return
        if command == "status":
            print(f"You have {hp} HP and {gold} gold. "
                  f"The {enemy_name} has {enemy_hp} HP.")
            continue
        if command != "attack":
            print("I don't know that command. Try: attack, status, quit.")
            continue

        # One combat round: you strike, then the enemy counters if alive.
        hp, enemy_hp = attack(hp, enemy_hp, rng)
        if enemy_hp <= 0:
            gold += reward()
            print(f"You slay the {enemy_name}! (+{reward()} gold)")
            if floor == final_floor:
                print(f"\nYou have cleared the dungeon with {hp} HP "
                      f"and {gold} gold. Victory!")
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
