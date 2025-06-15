from colorama import Fore
from core_game import catch_monster, calculate_catch_rate, get_player_collection
from models import MonsterSpecies
from sqlalchemy.sql.expression import func
import random

def create_player_cli(db):
    username = input("Enter new username: ")
    from battle_system import create_player
    player = create_player(db, username)
    if player:
        print(Fore.GREEN + f"Player '{username}' created successfully!")
    else:
        print(Fore.RED + "Failed to create player.")

def login_cli(db):
    username = input("Enter username: ")
    from battle_system import get_player_by_username
    player = get_player_by_username(db, username)
    if player:
        print(Fore.GREEN + f"Welcome back {username}!")
        player_session(db, player)
    else:
        print(Fore.RED + "Player not found.")

def player_session(db, player):
    while True:
        print(f"=== Welcome {player.username}! ===")
        print("1. Catch Monster")
        print("2. View Collection")
        print("3. Battle")
        print("4. Trade")
        print("5. Profile")
        print("6. Logout")
        choice = input("Choose an option: ")
        if choice == "1":
            catch_monster_cli(db, player)
        elif choice == "2":
            view_collection_cli(db, player)
        elif choice == "3":
            battle_cli(db, player)
        elif choice == "4":
            print("Trade feature coming soon.")
        elif choice == "5":
            view_profile_cli(player)
        elif choice == "6":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")

def catch_monster_cli(db, player):
    species = db.query(MonsterSpecies).order_by(func.random()).first()
    if not species:
        print("No monsters available to catch.")
        return
    print(f"You encounter a wild {species.name} ({species.type} {species.rarity})!")
    print("Attempting to catch...")
    success = catch_monster(db, player.id, species.id, player.level)
    if success:
        print(f"Success! {species.name} joined your team!")
    else:
        print(f"Oh no! The {species.name} escaped!")

def view_collection_cli(db, player):
    collection = get_player_collection(db, player.id)
    if not collection:
        print("Your collection is empty.")
        return
    print("Your Monster Collection:")
    for monster in collection:
        print(f"- {monster['species_name']} (Lv.{monster['level']}) HP: {monster['stats'].get('hp', 'N/A')}")

def view_profile_cli(player):
    print(f"Username: {player.username} Level: {player.level} Money: {player.money}")

def battle_cli(db, player):
    from battle_system import create_battle, execute_turn
    from core_game import get_player_collection
    print("=== Battle Menu ===")
    print("1. Battle Wild Monster")
    print("2. Battle Player")
    print("3. Back")
    choice = input("Choose an option: ")
    if choice == "1":
        battle_wild_monster_cli(db, player)
    elif choice == "2":
        print("Player battle feature coming soon.")
    elif choice == "3":
        return
    else:
        print("Invalid choice. Please try again.")

def battle_wild_monster_cli(db, player):
    import random
    from core_game import get_player_collection
    from battle_system import create_battle, execute_turn
    # Select a random wild monster species
    species = db.query(MonsterSpecies).order_by(func.random()).first()
    if not species:
        print("No wild monsters available.")
        return
    print(f"A wild {species.name} ({species.type}) appears!")
    # Create battle record
    battle = create_battle(db, player.id)
    # Select player's monster for battle
    collection = get_player_collection(db, player.id)
    if not collection:
        print("You have no monsters to battle with.")
        return
    print("Choose your monster for battle:")
    for idx, monster in enumerate(collection, 1):
        print(f"{idx}. {monster['species_name']} (Lv.{monster['level']}) HP: {monster['stats'].get('hp', 'N/A')}")
    choice = input("Enter choice: ")
    try:
        choice_idx = int(choice) - 1
        player_monster = collection[choice_idx]
    except (ValueError, IndexError):
        print("Invalid choice.")
        return
    # Create wild monster as PlayerMonster instance (not saved to DB)
    wild_monster = {
        'id': None,
        'species_name': species.name,
        'level': 1,
        'stats': {'hp': 30, 'attack': 10, 'defense': 5},
        'current_hp': 30
    }
    print(f"Battle begins! {player_monster['species_name']} vs {wild_monster['species_name']}")
    # Simple battle loop
    player_hp = player_monster['stats'].get('hp', 30)
    wild_hp = wild_monster['stats']['hp']
    while player_hp > 0 and wild_hp > 0:
        print(f"\nYour {player_monster['species_name']} HP: {player_hp}")
        print(f"Wild {wild_monster['species_name']} HP: {wild_hp}")
        print("Choose your action:")
        print("1. Attack")
        print("2. Defend")
        print("3. Run")
        action = input("Enter choice: ")
        if action == "1":
            damage = 10  # Simplified fixed damage
            wild_hp -= damage
            print(f"You dealt {damage} damage!")
        elif action == "2":
            print("You defend and reduce incoming damage this turn.")
        elif action == "3":
            print("You fled the battle.")
            return
        else:
            print("Invalid action.")
            continue
        if wild_hp <= 0:
            print("You won the battle!")
            break
        # Wild monster attacks
        damage = 8
        player_hp -= damage
        print(f"Wild {wild_monster['species_name']} dealt {damage} damage!")
        if player_hp <= 0:
            print("You lost the battle!")
            break

def main():
    from database import SessionLocal
    db = SessionLocal()
    while True:
        print("=== Monster Collection CLI Game ===")
        print("1. Create Player")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            create_player_cli(db)
        elif choice == "2":
            login_cli(db)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
