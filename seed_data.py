from database import SessionLocal
from models import MonsterSpecies

def seed_monster_species():
    db = SessionLocal()
    species_data = [
        {"name": "Flamewyrm", "type": "Fire", "base_stats": "{'hp': 45, 'attack': 60, 'defense': 40}", "rarity": "Common", "abilities": "Fire Blast"},
        {"name": "Aquafin", "type": "Water", "base_stats": "{'hp': 50, 'attack': 55, 'defense': 45}", "rarity": "Common", "abilities": "Water Pulse"},
        {"name": "Vinewhip", "type": "Grass", "base_stats": "{'hp': 40, 'attack': 50, 'defense': 50}", "rarity": "Common", "abilities": "Vine Whip"},
        {"name": "Sparkbolt", "type": "Electric", "base_stats": "{'hp': 35, 'attack': 65, 'defense': 30}", "rarity": "Rare", "abilities": "Thunderbolt"},
        {"name": "Rockgrinder", "type": "Rock", "base_stats": "{'hp': 60, 'attack': 70, 'defense': 60}", "rarity": "Uncommon", "abilities": "Rock Slide"},
        {"name": "Thunderwing", "type": "Electric", "base_stats": "{'hp': 55, 'attack': 75, 'defense': 40}", "rarity": "Rare", "abilities": "Thunder Punch"},
        {"name": "Megabolt", "type": "Electric", "base_stats": "{'hp': 70, 'attack': 90, 'defense': 60}", "rarity": "Epic", "abilities": "Mega Thunder"},
        {"name": "Rockjaw", "type": "Rock", "base_stats": "{'hp': 50, 'attack': 65, 'defense': 55}", "rarity": "Uncommon", "abilities": "Bite"},
        {"name": "Flareclaw", "type": "Fire", "base_stats": "{'hp': 45, 'attack': 70, 'defense': 35}", "rarity": "Rare", "abilities": "Flame Claw"},
        {"name": "Aquashield", "type": "Water", "base_stats": "{'hp': 60, 'attack': 50, 'defense': 70}", "rarity": "Uncommon", "abilities": "Water Shield"},
        {"name": "Leafdancer", "type": "Grass", "base_stats": "{'hp': 40, 'attack': 55, 'defense': 45}", "rarity": "Common", "abilities": "Leaf Dance"},
        {"name": "Voltstrike", "type": "Electric", "base_stats": "{'hp': 50, 'attack': 80, 'defense': 40}", "rarity": "Rare", "abilities": "Volt Strike"},
        {"name": "Stonehorn", "type": "Rock", "base_stats": "{'hp': 65, 'attack': 75, 'defense': 65}", "rarity": "Epic", "abilities": "Horn Attack"},
        {"name": "Firetail", "type": "Fire", "base_stats": "{'hp': 40, 'attack': 60, 'defense': 40}", "rarity": "Common", "abilities": "Tail Whip"},
        {"name": "Hydrofin", "type": "Water", "base_stats": "{'hp': 55, 'attack': 60, 'defense': 50}", "rarity": "Common", "abilities": "Hydro Pump"},
    ]

    for species in species_data:
        existing = db.query(MonsterSpecies).filter(MonsterSpecies.name == species["name"]).first()
        if not existing:
            new_species = MonsterSpecies(
                name=species["name"],
                type=species["type"],
                base_stats=species["base_stats"],
                rarity=species["rarity"],
                abilities=species["abilities"]
            )
            db.add(new_species)
    db.commit()
    db.close()
    print("Seeded monster species data.")

if __name__ == "__main__":
    seed_monster_species()
