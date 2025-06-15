from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime, Table
from sqlalchemy.orm import relationship
from database import Base
import datetime

# Association table for many-to-many relationship between Trades and Player_Monsters
trade_monsters_association = Table(
    'trade_monsters_association',
    Base.metadata,
    Column('trade_id', Integer, ForeignKey('trades.id')),
    Column('player_monster_id', Integer, ForeignKey('player_monsters.id'))
)

class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    level = Column(Integer, default=1)
    experience = Column(Integer, default=0)
    money = Column(Integer, default=0)
    achievements = relationship("PlayerAchievement", back_populates="player")
    monsters = relationship("PlayerMonster", back_populates="owner")
    battles = relationship("Battle", back_populates="player", foreign_keys='Battle.player_id')
    trades_sent = relationship("Trade", back_populates="from_player", foreign_keys='Trade.from_player_id')
    trades_received = relationship("Trade", back_populates="to_player", foreign_keys='Trade.to_player_id')

class MonsterSpecies(Base):
    __tablename__ = 'monster_species'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    type = Column(String, nullable=False)
    base_stats = Column(String)  # JSON string or serialized dict of stats
    rarity = Column(String)
    abilities = Column(String)  # Comma separated abilities or JSON string
    player_monsters = relationship("PlayerMonster", back_populates="species")

class PlayerMonster(Base):
    __tablename__ = 'player_monsters'

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey('players.id'))
    species_id = Column(Integer, ForeignKey('monster_species.id'))
    level = Column(Integer, default=1)
    experience = Column(Integer, default=0)
    current_hp = Column(Integer)
    stats = Column(String)  # JSON string or serialized dict of current stats
    owner = relationship("Player", back_populates="monsters")
    species = relationship("MonsterSpecies", back_populates="player_monsters")
    trades = relationship("Trade", secondary=trade_monsters_association, back_populates="monsters")

class Battle(Base):
    __tablename__ = 'battles'

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey('players.id'))
    opponent_id = Column(Integer, ForeignKey('players.id'), nullable=True)  # Null for wild battles
    result = Column(String)  # win, lose, draw
    date = Column(DateTime, default=datetime.datetime.utcnow)
    player = relationship("Player", back_populates="battles", foreign_keys=[player_id])

class Trade(Base):
    __tablename__ = 'trades'

    id = Column(Integer, primary_key=True, index=True)
    from_player_id = Column(Integer, ForeignKey('players.id'))
    to_player_id = Column(Integer, ForeignKey('players.id'))
    date = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String)  # pending, accepted, declined
    monsters = relationship("PlayerMonster", secondary=trade_monsters_association, back_populates="trades")
    from_player = relationship("Player", back_populates="trades_sent", foreign_keys=[from_player_id])
    to_player = relationship("Player", back_populates="trades_received", foreign_keys=[to_player_id])

class Achievement(Base):
    __tablename__ = 'achievements'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    players = relationship("PlayerAchievement", back_populates="achievement")

class PlayerAchievement(Base):
    __tablename__ = 'player_achievements'

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey('players.id'))
    achievement_id = Column(Integer, ForeignKey('achievements.id'))
    progress = Column(Integer, default=0)
    unlocked = Column(Boolean, default=False)
    player = relationship("Player", back_populates="achievements")
    achievement = relationship("Achievement", back_populates="players")
