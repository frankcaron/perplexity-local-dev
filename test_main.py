"""Tests for the dungeon crawler: combat rules (rpg) and the CLI game loop (main)."""

import io
import random
import sys
from contextlib import redirect_stdout

import main
from rpg import ENEMIES, attack, pick_enemy, reward


# --------------------------------------------------------------------------
# rpg: combat rules
# --------------------------------------------------------------------------

def test_pick_enemy_uses_floor_index_clamped_to_table():
    rng = random.Random(1)
    assert pick_enemy(rng, 1) == ENEMIES[0]
    assert pick_enemy(rng, 3) == ENEMIES[2]
    # Floors past the end of the table reuse the strongest enemy.
    assert pick_enemy(rng, 99) == ENEMIES[-1]


def test_attack_deals_damage_and_counters_when_enemy_survives():
    player_hp, enemy_hp = attack(50, 45, random.Random(1))
    assert (player_hp, enemy_hp) == (46, 33)


def test_attack_does_not_counter_when_enemy_dies():
    player_hp, enemy_hp = attack(50, 10, random.Random(1))
    assert (player_hp, enemy_hp) == (50, 0)


def test_attack_clamps_hit_points_at_zero():
    assert attack(2, 100, random.Random(1)) == (0, 88)


def test_reward_is_fixed_gold_amount():
    assert reward() == 10


# --------------------------------------------------------------------------
# main: game loop driven through stdin/stdout
# --------------------------------------------------------------------------

def run_game(commands: list[str]) -> str:
    """Play ``commands`` through the game and return the captured output."""
    stdin = io.StringIO("\n".join(commands) + "\n")
    buffer = io.StringIO()
    old_stdin = sys.stdin
    sys.stdin = stdin
    try:
        with redirect_stdout(buffer):
            main.play(random.Random(42))
    finally:
        sys.stdin = old_stdin
    return buffer.getvalue()


def test_game_ends_gracefully_on_eof():
    output = run_game([])
    assert "You leave the dungeon" in output


def test_game_ends_on_quit():
    output = run_game(["quit"])
    assert "You leave the dungeon" in output


def test_unknown_command_is_rejected_and_game_continues():
    output = run_game(["frob", "quit"])
    assert "I don't know that command" in output
    assert "You leave the dungeon" in output


def test_status_reports_current_state():
    output = run_game(["status", "quit"])
    assert "You have 50 HP and 0 gold" in output
    assert "giant rat has 20 HP" in output


def test_attacking_weak_enemy_defeats_it_and_advances_floor():
    # The giant rat (20 HP) dies to two 12-damage strikes: 20 -> 8 -> 0.
    # The second strike lands on a dead enemy, so the player takes no counter.
    output = run_game(["attack", "attack", "status"])
    assert "You slay the giant rat! (+10 gold)" in output
    assert "You descend to floor 2" in output
    assert "You have 46 HP and 10 gold" in output
    assert "cave bat has 25 HP" in output


def test_full_dungeon_clear_is_a_victory():
    # 12 damage per hit vs. enemy HP 20/25/35/45/60 needs 2/3/3/4/5 hits,
    # 17 attacks total; each enemy counters for 4 damage on every round it
    # survives, so the player finishes the dungeon at 2 HP.
    output = run_game(["attack"] * 17)
    assert "Victory!" in output
    assert "2 HP" in output
    assert "50 gold" in output
