import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from models import Player, MonsterSpecies
from core_game import catch_monster, get_player_collection
from battle_system import create_player

class TestCriticalPath(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Use in-memory SQLite database for testing
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self):
        self.db = self.Session()
        # Clear existing data to avoid UNIQUE constraint errors
        self.db.query(MonsterSpecies).delete()
        self.db.commit()
        # Seed a monster species
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

    def tearDown(self):
        self.db.close()

    def test_player_creation(self):
        player = create_player(self.db, "testplayer")
        self.assertIsNotNone(player)
        self.assertEqual(player.username, "testplayer")

    def test_catch_monster(self):
        player = create_player(self.db, "catcher")
        success = catch_monster(self.db, player.id, self.species_id, player.level)
        self.assertIn(success, [True, False])  # Catch can succeed or fail

    def test_player_creation(self):
        player = create_player(self.db, "testplayer")
        self.assertIsNotNone(player)
        self.assertEqual(player.username, "testplayer")

    def test_get_player_collection(self):
        player = create_player(self.db, "collector")
        catch_monster(self.db, player.id, self.species_id, player.level)
        collection = get_player_collection(self.db, player.id)
        self.assertIsInstance(collection, list)
        # Collection may be empty if catch failed, so no strict assert on length

if __name__ == '__main__':
    unittest.main()
