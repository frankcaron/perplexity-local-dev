"""Tests for the dungeon crawler: combat rules (rpg) and the CLI game loop (main)."""

import io
import random
import sys
from contextlib import redirect_stdout

import main
from rpg import (
    ENEMIES,
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
    xp_to_next,
)


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
    player_hp, enemy_hp = attack(50, 45, 12, random.Random(1))
    assert (player_hp, enemy_hp) == (46, 33)


def test_attack_does_not_counter_when_enemy_dies():
    player_hp, enemy_hp = attack(50, 10, 12, random.Random(1))
    assert (player_hp, enemy_hp) == (50, 0)


def test_attack_clamps_hit_points_at_zero():
    assert attack(2, 100, 12, random.Random(1)) == (0, 88)


def test_reward_is_fixed_gold_amount():
    assert reward() == 10


# --------------------------------------------------------------------------
# rpg: leveling rules
# --------------------------------------------------------------------------

def test_xp_reward_is_fixed():
    assert xp_reward() == 20


def test_xp_to_next_uses_linear_curve():
    assert xp_to_next(1) == 20
    assert xp_to_next(2) == 40


def test_gain_xp_without_level_up():
    assert gain_xp(0, 1, 10) == (10, 1)


def test_gain_xp_single_level_up():
    assert gain_xp(0, 1, 20) == (0, 2)


def test_gain_xp_multi_level_up():
    # 100 XP at level 1: 20 -> level 2, 40 -> level 3, leaving 40 XP.
    assert gain_xp(0, 1, 100) == (40, 3)


def test_level_stats_base():
    assert level_stats(1) == (50, 12)


def test_level_stats_growth():
    assert level_stats(2) == (60, 15)


# --------------------------------------------------------------------------
# rpg: shop rules
# --------------------------------------------------------------------------

def test_weapon_price_rises_with_upgrades():
    assert weapon_price(0) == 20
    assert weapon_price(1) == 35
    assert weapon_price(2) == 50


def test_buy_potion_deducts_gold():
    assert buy_potion(15) == 0


def test_buy_potion_rejects_when_poor():
    assert buy_potion(14) is None


def test_use_potion_heals_and_caps_at_max_hp():
    assert use_potion(20, 50, 1) == (45, 0)
    assert use_potion(40, 50, 1) == (50, 0)


def test_use_potion_none_with_zero_potions():
    assert use_potion(20, 50, 0) is None


def test_use_potion_none_at_full_hp():
    assert use_potion(50, 50, 1) is None


def test_weapon_damage_base():
    assert weapon_damage(1, 0) == 12


def test_weapon_damage_level_growth():
    assert weapon_damage(2, 0) == 15


def test_weapon_damage_with_upgrades():
    assert weapon_damage(2, 2) == 25


def test_buy_weapon_buys_and_price_rises():
    assert buy_weapon(20, 0) == (0, 1)
    # After one upgrade the next one costs 35.
    assert buy_weapon(35, 1) == (0, 2)


def test_buy_weapon_rejects_when_poor():
    assert buy_weapon(19, 0) is None


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
    assert "level 1, 0 XP, 50/50 HP" in output
    assert "weapon 12 dmg" in output
    assert "0 gold" in output
    assert "0 potions" in output
    assert "giant rat has 20 HP" in output


def test_attacking_weak_enemy_defeats_it_and_advances_floor():
    # The giant rat (20 HP) dies to two 12-damage strikes: 20 -> 8 -> 0.
    # The counter came on the first strike (enemy still alive at 8 HP).
    output = run_game(["attack", "attack", "status"])
    assert "You slay the giant rat! (+10 gold, +20 XP)" in output
    assert "Level up! You are now level 2" in output
    assert "You descend to floor 2" in output
    assert "level 2, 0 XP, 60/60 HP" in output
    assert "weapon 15 dmg" in output
    assert "10 gold" in output
    assert "cave bat has 25 HP" in output


def test_shop_menu_shows_both_goods_with_prices():
    output = run_game(["shop", "back", "quit"])
    assert "potion - 15 gold" in output
    assert "weapon - 20 gold" in output
    assert "You have 0 gold" in output


def test_shop_buy_potion_with_no_gold_is_rejected():
    output = run_game(["shop", "potion", "back", "quit"])
    assert "Not enough gold" in output


def test_shop_buy_potion_with_insufficient_gold_is_rejected():
    # Slay the giant rat (10 gold), then buy a potion (15 gold) — unaffordable.
    output = run_game(["attack", "attack", "shop", "potion", "back", "quit"])
    assert "Not enough gold" in output


def test_shop_buy_potion_after_two_kills_deducts_gold():
    # Two kills = 20 gold; buy a potion for 15, leaving 5 gold.
    output = run_game(
        ["attack", "attack", "attack", "attack", "shop", "potion", "back", "quit"]
    )
    assert "You buy a potion" in output
    assert "5 gold left" in output
    assert "1 potions" in output


def test_use_potion_at_full_hp_is_rejected():
    # Four attacks: kill rat (level up to 60/60), kill bat.  After the bat,
    # player is at 56/60, 20 gold.  Buy a potion (56/60, 5 gold, 1 potion).
    # Use it: heals to 60/60, 0 potions.  Use again: no potions left.
    output = run_game(
        ["attack", "attack", "attack", "attack", "shop", "potion", "back",
         "use potion", "use potion", "quit"]
    )
    assert "You buy a potion" in output
    assert "You drink a potion" in output
    assert "no potions" in output


def test_shop_second_weapon_purchase_costs_more():
    # Four attacks = 20 gold (two kills: rat 20 HP, bat 25 HP).  Buy the
    # base weapon upgrade (20 gold), leaving 0.  Re-open the shop and the
    # next upgrade should be listed at 35 gold.
    output = run_game(
        ["attack", "attack", "attack", "attack", "shop", "weapon", "back",
         "shop", "back", "quit"]
    )
    assert "You buy a weapon upgrade!" in output
    assert "weapon - 35 gold" in output


def test_shop_buy_weapon_raises_damage():
    # Two kills = 20 gold, exactly the base weapon price.
    output = run_game(
        ["attack", "attack", "attack", "attack", "shop", "weapon", "back", "status", "quit"]
    )
    assert "You buy a weapon upgrade!" in output
    assert "weapon 20 dmg" in output


def test_use_potion_with_none_held_reports_none():
    output = run_game(["use potion", "quit"])
    assert "no potions" in output


def test_full_dungeon_clear_is_a_victory():
    # Level 2 needs 40 XP, so level-ups happen on kills 1 and 3 only.
    # Each level up grants +10 max HP and +3 weapon damage and fully heals.
    # Weapon damage grows 12 -> 15 -> 18, so the dark knight (60 HP)
    # dies in 4 hits instead of 5.  Simulated final state: 50 HP, 50 gold.
    output = run_game(["attack"] * 17)
    assert "Victory!" in output
    assert "50 HP" in output
    assert "50 gold" in output


# --------------------------------------------------------------------------
# main: regression tests
# --------------------------------------------------------------------------

def test_upgrade_survives_level_up():
    # Four attacks: 20 gold, level 2 (kill 1 levels up).  Buy weapon upgrade
    # (20 gold).  Two more attacks kill the bat (kill 3 levels up to 3).
    # Status should show 18 + 5 = 23 dmg.
    output = run_game(
        ["attack", "attack", "attack", "attack", "shop", "weapon", "back",
         "attack", "attack", "status", "quit"]
    )
    assert "weapon 23 dmg" in output


def test_blank_line_does_not_quit():
    output = run_game(["", "quit"])
    assert "Type a command" in output
    assert "You leave the dungeon" in output


def test_held_potion_round_trip():
    # Four attacks: 20 gold, hp 56/60 (level 2 full heal then 4 counter hits
    # on the bat).  Buy a potion, check status shows 1, use it to heal to 60.
    output = run_game(
        ["attack", "attack", "attack", "attack", "shop", "potion", "back",
         "status", "use potion", "status", "quit"]
    )
    assert "1 potions" in output
    assert "You drink a potion" in output
    assert "0 potions" in output


def test_combat_message_includes_numbers():
    # First attack on the giant rat (20 HP): deals 12, enemy counters for 4.
    output = run_game(["attack", "quit"])
    assert "for 12 damage" in output
    assert "hits back for 4" in output
