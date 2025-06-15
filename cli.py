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
    print("=== Battle Menu ===")
    print("1. Battle Wild Monster")
    print("2. Battle Player")
    print("3. Back")
    choice = input("Choose an option: ")
    if choice == "1":
        print("Wild battle feature coming soon.")
    elif choice == "2":
        print("Player battle feature coming soon.")
    elif choice == "3":
        return
    else:
        print("Invalid choice. Please try again.")

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
