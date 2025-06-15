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
        # Create monsters for battle
        # Force catch_monster to always succeed by patching random.random
        import random
        original_random = random.random
        random.random = lambda: 0.0  # Always less than catch rate to ensure success
        catch_monster(self.db, self.player1.id, self.species_id, self.player1.level)
        catch_monster(self.db, self.player2.id, self.species_id, self.player2.level)
        random.random = original_random  # Restore original function
        self.db.commit()  # Commit to save monsters
        attacker_monster = self.db.query(PlayerMonster).filter(PlayerMonster.player_id == self.player1.id).first()
        defender_monster = self.db.query(PlayerMonster).filter(PlayerMonster.player_id == self.player2.id).first()
        battle = create_battle(self.db, self.player1.id, self.player2.id)
        self.assertIsNotNone(battle)
        result = execute_turn(self.db, battle.id, attacker_monster.id, defender_monster.id, "Attack")
        self.assertIn('damage', result)

    def test_trade_proposal(self):
        import logging
        logging.basicConfig(level=logging.DEBUG)
        logger = logging.getLogger(__name__)
        # Create monsters for trade
        # Force catch_monster to always succeed by patching random.random
        import random
        original_random = random.random
        random.random = lambda: 0.0  # Always less than catch rate to ensure success
        catch_monster(self.db, self.player1.id, self.species_id, self.player1.level)
        catch_monster(self.db, self.player2.id, self.species_id, self.player2.level)
        random.random = original_random  # Restore original function
        self.db.commit()
        offered_monster = self.db.query(PlayerMonster).filter(PlayerMonster.player_id == self.player1.id).first()
        requested_monster = self.db.query(PlayerMonster).filter(PlayerMonster.player_id == self.player2.id).first()
        logger.debug(f"Offered monster: {offered_monster}")
        logger.debug(f"Requested monster: {requested_monster}")
        if not offered_monster or not requested_monster:
            self.fail("Failed to create player monsters for trade test")
        trade = propose_trade(self.db, self.player1.id, self.player2.id, [offered_monster.id], [requested_monster.id])
        self.assertIsNotNone(trade)
        self.assertEqual(trade.status, 'pending')

    def test_level_up_monster(self):
        # Force catch_monster to always succeed by patching random.random
        import random
        original_random = random.random
        random.random = lambda: 0.0  # Always less than catch rate to ensure success
        catch_monster(self.db, self.player1.id, self.species_id, self.player1.level)
        random.random = original_random  # Restore original function
        monster = self.db.query(PlayerMonster).filter(PlayerMonster.player_id == self.player1.id).first()
        if not monster:
            self.fail("Failed to create player monster for level up test")
        old_level = monster.level
        level_up_monster(self.db, monster.id)
        self.db.refresh(monster)
        self.assertEqual(monster.level, old_level + 1)

if __name__ == '__main__':
    unittest.main()
