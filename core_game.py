import random
from models import PlayerMonster, MonsterSpecies
from sqlalchemy.orm import Session

# Type effectiveness chart
TYPE_EFFECTIVENESS = {
    'Fire': {'Grass': 2.0, 'Water': 0.5, 'Air': 1.0, 'Earth': 1.0},
    'Water': {'Fire': 2.0, 'Earth': 1.5, 'Air': 1.0, 'Grass': 0.5},
    'Grass': {'Water': 2.0, 'Fire': 0.5, 'Earth': 1.0, 'Air': 1.0},
    'Electric': {'Water': 2.0, 'Earth': 0.0, 'Air': 1.5, 'Fire': 1.0},
    'Air': {'Earth': 2.0, 'Electric': 0.5, 'Fire': 1.0, 'Water': 1.0},
    'Earth': {'Fire': 2.0, 'Electric': 1.5, 'Air': 0.5, 'Grass': 1.0},
}

def calculate_type_effectiveness(attacker_type: str, defender_type: str) -> float:
    return TYPE_EFFECTIVENESS.get(attacker_type, {}).get(defender_type, 1.0)

def calculate_catch_rate(species_rarity: str, player_level: int) -> float:
    rarity_rates = {
        'Common': 0.7,
        'Uncommon': 0.5,
        'Rare': 0.3,
        'Epic': 0.15,
        'Legendary': 0.05
    }
    base_rate = rarity_rates.get(species_rarity, 0.5)
    level_bonus = min(player_level / 100, 0.3)  # max 0.3 bonus
    return min(base_rate + level_bonus, 0.95)

def catch_monster(db: Session, player_id: int, species_id: int, player_level: int) -> bool:
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    species = db.query(MonsterSpecies).filter(MonsterSpecies.id == species_id).first()
    if not species:
        logger.debug(f"No species found with id {species_id}")
        return False
    catch_rate = calculate_catch_rate(species.rarity, player_level)
    success = random.random() < catch_rate
    logger.debug(f"Catch rate: {catch_rate}, success: {success}")
    if success:
        # Convert base_stats string to dict safely
        import ast
        base_stats = ast.literal_eval(species.base_stats) if species.base_stats else {}
        new_monster = PlayerMonster(
            player_id=player_id,
            species_id=species_id,
            level=1,
            experience=0,
            current_hp=base_stats.get('hp', 10),
            stats=str(base_stats)  # Store as string for now
        )
        db.add(new_monster)
        db.flush()  # Use flush instead of commit here
        db.commit()
        logger.debug(f"New monster added: {new_monster}")
    return success

def level_up_monster(db: Session, monster_id: int) -> dict:
    monster = db.query(PlayerMonster).filter(PlayerMonster.id == monster_id).first()
    if not monster:
        return {}
    monster.level += 1
    # Simple stat increase example
    base_stats = eval(monster.stats)  # Convert string back to dict
    base_stats['hp'] = base_stats.get('hp', 10) + 5 * monster.level
    monster.stats = str(base_stats)
    monster.current_hp = base_stats['hp']
    db.commit()
    return {'level': monster.level, 'stats': base_stats}

def get_player_collection(db: Session, player_id: int) -> list:
    monsters = db.query(PlayerMonster).filter(PlayerMonster.player_id == player_id).all()
    collection = []
    for m in monsters:
        species = db.query(MonsterSpecies).filter(MonsterSpecies.id == m.species_id).first()
        collection.append({
            'monster_id': m.id,
            'species_name': species.name if species else 'Unknown',
            'level': m.level,
            'current_hp': m.current_hp,
            'stats': eval(m.stats) if m.stats else {}
        })
    return collection
