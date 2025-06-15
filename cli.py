import sys
from colorama import init, Fore, Style
from database import SessionLocal
from core_game import catch_monster, get_player_collection
from battle_system import create_player, get_player

init(autoreset=True)

def main_menu():
    print(Fore.CYAN + "=== Monster Collection CLI Game ===")
    print("1. Create Player")
    print("2. Login")
    print("3. Exit")

def player_menu(username):
    print(Fore.GREEN + f"=== Welcome, {username}! ===")
    print("1. Catch Monster")
    print("2. View Collection")
    print("3. Battle")
    print("4. Trade")
    print("5. Profile")
    print("6. Logout")

def create_player_cli(db):
    username = input("Enter new username: ")
    player = create_player(db, username)
    print(Fore.YELLOW + f"Player '{player.username}' created successfully!")

def login_cli(db):
    username = input("Enter username: ")
    player = get_player(db, username)
    if player:
        print(Fore.YELLOW + f"Welcome back, {player.username}!")
        player_session(db, player)
    else:
        print(Fore.RED + "Player not found.")

from core_game import catch_monster, calculate_catch_rate
import random
from models import MonsterSpecies
from sqlalchemy.sql.expression import func

def catch_monster_cli(db, player):
    # Simulate encountering a random monster species
    species = db.query(MonsterSpecies).order_by(func.random()).first()
    if not species:
        print("No monsters available to catch.")
        return
    print(f"You encounter a wild {species.name} ({species.type}, {species.rarity})!")
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
    print(Fore.MAGENTA + "Your Monster Collection:")
    for m in collection:
        print(f"- {m['species_name']} (Lv.{m['level']}) HP: {m['current_hp']}")

def player_session(db, player):
    while True:
        player_menu(player.username)
        choice = input("Choose an option: ")
        if choice == '1':
            catch_monster_cli(db, player)
        elif choice == '2':
            view_collection_cli(db, player)
        elif choice == '3':
            print("Battle feature coming soon.")
        elif choice == '4':
            print("Trade feature coming soon.")
        elif choice == '5':
            print(f"Username: {player.username}, Level: {player.level}, Money: {player.money}")
        elif choice == '6':
            print("Logging out...")
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again.")

def main():
    db = SessionLocal()
    while True:
        main_menu()
        choice = input("Choose an option: ")
        if choice == '1':
            create_player_cli(db)
        elif choice == '2':
            login_cli(db)
        elif choice == '3':
            print("Goodbye!")
            db.close()
            sys.exit()
        else:
            print(Fore.RED + "Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
