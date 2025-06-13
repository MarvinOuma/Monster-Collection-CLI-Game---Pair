from models import Player, Battle, PlayerMonster, Trade
from sqlalchemy.orm import Session
import random
import datetime

def create_player(db: Session, username: str) -> Player:
    player = Player(username=username, level=1, experience=0, money=100)
    db.add(player)
    db.commit()
    db.refresh(player)
    return player

def get_player(db: Session, username: str) -> Player:
    return db.query(Player).filter(Player.username == username).first()

def create_battle(db: Session, player1_id: int, player2_id: int, monster_teams: list) -> Battle:
    battle = Battle(player_id=player1_id, opponent_id=player2_id, result='ongoing', date=datetime.datetime.utcnow())
    db.add(battle)
    db.commit()
    db.refresh(battle)
    # Additional logic to store monster teams can be added here
    return battle

def execute_turn(db: Session, battle_id: int, attacker_monster_id: int, defender_monster_id: int, move: str) -> dict:
    # Simplified turn execution logic
    # Fetch monsters
    attacker = db.query(PlayerMonster).filter(PlayerMonster.id == attacker_monster_id).first()
    defender = db.query(PlayerMonster).filter(PlayerMonster.id == defender_monster_id).first()
    if not attacker or not defender:
        return {'error': 'Invalid monster IDs'}

    # Calculate damage (placeholder)
    damage = 10  # Simplified fixed damage
    defender.current_hp = max(defender.current_hp - damage, 0)
    db.commit()

    return {
        'attacker_id': attacker_monster_id,
        'defender_id': defender_monster_id,
        'damage': damage,
        'defender_hp': defender.current_hp
    }

def check_battle_end(db: Session, battle_id: int) -> bool:
    # Placeholder logic to check if battle ended
    battle = db.query(Battle).filter(Battle.id == battle_id).first()
    if not battle:
        return True
    # Implement actual logic based on monster HP or other conditions
    return False

def apply_status_effects(db: Session, monster_id: int, effect_type: str) -> None:
    # Placeholder for status effect application
    pass

def propose_trade(db: Session, from_player_id: int, to_player_id: int, offered_monsters: list, requested_monsters: list) -> Trade:
    trade = Trade(from_player_id=from_player_id, to_player_id=to_player_id, status='pending', date=datetime.datetime.utcnow())
    db.add(trade)
    db.commit()
    db.refresh(trade)
    # Logic to link monsters to trade can be added here
    return trade

def calculate_battle_rewards(winner_id: int, battle_difficulty: int) -> tuple:
    # Simplified reward calculation
    exp = 50 * battle_difficulty
    money = 100 * battle_difficulty
    return (exp, money)

def create_ai_opponent(difficulty_level: int) -> dict:
    # Placeholder AI opponent creation
    return {
        'name': f'AI_Level_{difficulty_level}',
        'monster_team': []
    }
