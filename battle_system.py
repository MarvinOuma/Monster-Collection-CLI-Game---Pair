from models import Battle, PlayerMonster, Player
from sqlalchemy.orm import joinedload
from sqlalchemy import and_
import random

def create_player(db, username):
    player = Player(username=username, level=1, experience=0, money=100)
    db.add(player)
    db.commit()
    db.refresh(player)
    return player

def get_player_by_username(db, username):
    return db.query(Player).filter(Player.username == username).first()

def create_battle(db, player_id, opponent_id=None, result=None):
    if opponent_id == []:
        opponent_id = None
    if result == []:
        result = None
    battle = Battle(player_id=player_id, opponent_id=opponent_id, result=result)
    db.add(battle)
    db.commit()
    db.refresh(battle)
    return battle

def execute_turn(db, battle_id, attacker_monster_id, defender_monster_id, move):
    # Simplified turn execution logic
    attacker = db.query(PlayerMonster).get(attacker_monster_id)
    defender = db.query(PlayerMonster).get(defender_monster_id)
    if not attacker or not defender:
        return {"error": "Invalid monster IDs"}

    # Calculate damage (simplified)
    damage = max(0, attacker.level * 5 - defender.level * 3)
    defender.current_hp = max(0, defender.current_hp - damage)
    db.commit()

    result = {
        "attacker": attacker.id,
        "defender": defender.id,
        "damage": damage,
        "defender_hp": defender.current_hp
    }
    return result

def calculate_damage(attacker_stats, defender_stats, move_power, type_effectiveness):
    base_damage = (attacker_stats['attack'] * move_power) - defender_stats['defense']
    damage = max(1, int(base_damage * type_effectiveness))
    return damage

def check_battle_end(db, battle_id):
    battle = db.query(Battle).get(battle_id)
    if not battle:
        return False
    # Check if any player's monsters have all fainted
    # Simplified: if any monster has hp > 0, battle continues
    player1_monsters = db.query(PlayerMonster).filter(PlayerMonster.player_id == battle.player1_id).all()
    player2_monsters = db.query(PlayerMonster).filter(PlayerMonster.player_id == battle.player2_id).all()
    p1_alive = any(m.current_hp > 0 for m in player1_monsters)
    p2_alive = any(m.current_hp > 0 for m in player2_monsters)
    if not p1_alive or not p2_alive:
        battle.status = 'finished'
        db.commit()
        return True
    return False

def apply_status_effects(monster_id, effect_type):
    # Placeholder for status effect application
    pass

def propose_trade(db, from_player_id, to_player_id, offered_monsters, requested_monsters):
    from models import Trade, PlayerMonster, Player
    from_player = db.query(Player).get(from_player_id)
    to_player = db.query(Player).get(to_player_id)
    offered_monster_objs = db.query(PlayerMonster).filter(PlayerMonster.id.in_(offered_monsters)).all()
    requested_monster_objs = db.query(PlayerMonster).filter(PlayerMonster.id.in_(requested_monsters)).all()
    trade = Trade(
        from_player=from_player,
        to_player=to_player,
        status='pending'
    )
    trade.monsters.extend(offered_monster_objs)
    trade.monsters.extend(requested_monster_objs)
    db.add(trade)
    db.commit()
    db.refresh(trade)
    return trade

def calculate_battle_rewards(winner_id, battle_difficulty):
    # Simplified reward calculation
    exp = 50 * battle_difficulty
    money = 100 * battle_difficulty
    return exp, money

def create_ai_opponent(difficulty_level):
    # Placeholder for AI opponent creation
    return {"name": f"AI Level {difficulty_level}", "team": []}
