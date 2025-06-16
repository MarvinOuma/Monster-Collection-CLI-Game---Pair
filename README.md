# Monster Collection CLI Game

## Project Overview
This is a text-based monster collection game inspired by Pokémon, implemented as a Command Line Interface (CLI) application with persistent data storage using SQLAlchemy and SQLite.

Players can catch, train, battle, and trade monsters. The game features a turn-based battle system with type effectiveness, player progression, and a trading system.

## Features Implemented
- Monster catching with rarity-based catch rates
- Monster training and leveling system
- Turn-based battle system with attack, defend, and run options
- Player vs Wild monster battles
- Player profiles with experience, level, and money
- Trading system between players
- Persistent data storage with SQLAlchemy ORM
- CLI interface with menus for catching, battling, trading, and profile management

## Player Progression
- Players gain experience and money by winning battles.
- Leveling up increases player stats and unlocks new features (to be implemented).
- Money can be used to purchase items or upgrades (future feature).

## Battle System
- Turn-based combat with simple attack and defend mechanics.
- Wild monsters appear randomly during exploration.
- Players select monsters from their collection to battle.
- Battle rewards include experience points and money based on difficulty.

## Trading System
- Players can propose trades offering and requesting monsters.
- Trades are tracked and managed through the database.

## CLI Commands
- Create Player: Register a new player profile.
- Login: Access existing player profile.
- Catch Monster: Encounter and attempt to catch wild monsters.
- View Collection: View owned monsters with stats.
- Battle: Engage in battles with wild monsters or other players (player battles coming soon).
- Trade: Propose and manage trades (basic implementation).
- Profile: View player stats and progress.

## Setup Instructions
1. Ensure Python 3.8+ is installed.
2. Install pipenv if not already installed: `pip install pipenv`
3. Install dependencies and activate virtual environment:
   ```
   pipenv install
   pipenv shell
   ```
4. Run the game:
   ```
   python monster_game.py
   ```

## Future Improvements
- Implement player vs player battles.
- Add shop and item system using in-game money.
- Enhance battle mechanics with special moves and status effects.
- Add monster evolution and breeding.
- Implement achievements and leaderboards.
- Improve CLI UX with colorful output and ASCII art.

## Testing
- Unit tests cover core game engine, battle system, and trade functionality.
- Run tests with:
  ```
  pipenv run python -m unittest discover tests
  ```

## License
This project is licensed under the MIT License.

---

Good luck, monster trainers!
