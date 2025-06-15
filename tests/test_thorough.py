import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from models import Player, Battle, Trade, PlayerMonster, MonsterSpecies, Achievement, PlayerAchievement
from core_game import catch_monster, get_player_collection, level_up_monster
from battle_system import create_player, create_battle, execute_turn, propose_trade

class TestThorough(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self):
        self.db = self.Session()
        self.db.query(MonsterSpecies).delete()
        self.db.query(Player).delete()
        self.db.query(Battle).delete()
        self.db.query(Trade).delete()
        self.db.query(PlayerMonster).delete()
        self.db.query(Achievement).delete()
        self.db.query(PlayerAchievement).delete()
        self.db.commit()

        # Seed monster species
        species = MonsterSpecies(
            name="Testmon",
            type="Fire",
            base_stats="{'hp': 30, 'attack': 10}",
            rarity="Common",
            abilities="Flame"
        )
        self.db.add(species)
        self.db.commit()
        self.species_id = species.id

        # Create players
        self.player1 = create_player(self.db, "player1")
        self.player2 = create_player(self.db, "player2")

    def tearDown(self):
        self.db.close()

    def test_battle_creation_and_turn(self):
        battle = create_battle(self.db, self.player1.id, self.player2.id, [])
        self.assertIsNotNone(battle)
        # Add monsters for battle
        catch_monster(self.db, self.player1.id, self.species_id, self.player1.level)
        catch_monster(self.db, self.player2.id, self.species_id, self.player2.level)
        self.db.commit()  # Commit to save monsters
        attacker_monster = self.db.query(PlayerMonster).filter(PlayerMonster.player_id == self.player1.id).first()
        defender_monster = self.db.query(PlayerMonster).filter(PlayerMonster.player_id == self.player2.id).first()
        result = execute_turn(self.db, battle.id, attacker_monster.id, defender_monster.id, "Attack")
        self.assertIn('damage', result)

    def test_trade_proposal(self):
        trade = propose_trade(self.db, self.player1.id, self.player2.id, [], [])
        self.assertIsNotNone(trade)
        self.assertEqual(trade.status, 'pending')

    def test_level_up_monster(self):
        catch_monster(self.db, self.player1.id, self.species_id, self.player1.level)
        monster = self.db.query(PlayerMonster).filter(PlayerMonster.player_id == self.player1.id).first()
        old_level = monster.level
        level_up_monster(self.db, monster.id)
        self.db.refresh(monster)
        self.assertEqual(monster.level, old_level + 1)

if __name__ == '__main__':
    unittest.main()
