import select
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Column, Integer, relationship, String, ForeignKey , VARCHAR
from model.game import Game
from model.player import Player
from model.battlefield import Battlefield

engine = create_engine('sqlite:////tmp/tdlog.db', echo=True, future=True)
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)

class GameEntity(Base):
 __tablename__ = 'game'
 id = Column(Integer, primary_key=True)
 players = relationship("PlayerEntity", back_populates="game", cascade="all, delete-orphan")

class PlayerEntity(Base):
 __tablename__ = 'player'
 id = Column(Integer, primary_key=True)
 name = Column(String, nullable=False)
 game_id = Column(Integer, ForeignKey("game.id"), nullable=False)
 game = relationship("GameEntity", back_populates="players")
 battle_field = relationship("BattlefieldEntity",
 back_populates="player", uselist=False, cascade="all, delete-orphan")

class BattlefieldEntity(Base):
 __tablename__= 'Battlefield'
 id = Column(Integer, primary_key=True, nullable= False)
 min_x = Column(Integer)
 min_y = Column(Integer)
 min_z = Column(Integer)
 max_x = Column(Integer)
 max_y = Column(Integer)
 max_z = Column(Integer)
 max_power = Column(Integer)
 player_id = Column(Integer, ForeignKey("Player.id"), nullable= False)
 player = relationship("PlayerEntity", back_populates= "battlefield", cascade="all, delete-orphan")


class VesselEntity(Base):
    __tablename__= 'Vessel'
    id = Column(Integer, primary_key=True, nullable= False)
    coord_x = Column(Integer)
    coord_y = Column(Integer)
    coord_z = Column(Integer)
    hits_to_be_destroyed = Column(Integer)
    type = Column(VARCHAR)
    battle_field_id= Column(Integer, ForeignKey("battlefield.id"), nullable= False)
    battle_field= relationship("BattlefieldEntity", back_populates="Vessel", cascade="all, delete-orphan")

class WeaponEntity(Base):
    __tablename__= 'Weapon'
    id= Column(Integer, primary_key= True, nullable= False)
    ammunitions= Column(Integer)
    range= Column(Integer)
    type= Column(VARCHAR)
    vessel_id= Column(Integer,ForeignKey("Vessel.id"),nullable= False)
    Vessel= relationship("VesselEntity", back_populates="Weapon", cascade="all, delete-orphan")

class GameDao:
    def __init__(self):
        Base.metadata.create_all()
        self.db_session = Session()
    def create_game(self, game: Game) -> int:
        game_entity = map_to_game_entity(game)
        self.db_session.add(game_entity)
        self.db_session.commit()
        return game_entity.id
    def find_game(self, game_id: int) -> Game:
        stmt = select(GameEntity).where(GameEntity.id == game_id)
        game_entity = self.db_session.scalars(stmt).one()
        return map_to_game(game_entity)

def map_to_game_entity(game: Game) -> GameEntity:
    game_entity = GameEntity(id=game.get_id())
    game_entity.players = [map_to_player_entity(player) for player in game.get_players()]
    return game_entity

def map_to_player_entity(player: Player) -> PlayerEntity:
    player_entity = PlayerEntity(
        id=player.get_id(),
        name=player.get_name()
    )
    return player_entity

def map_to_game(game_entity: GameEntity) -> Game:
    game = Game(id=game_entity.id)
    game.players = [map_to_player(player_entity) for player_entity in game_entity.players]
    return game

def map_to_player(player_entity: PlayerEntity) -> Player:
    player = Player(
        id=player_entity.id,
        name=player_entity.name
    )
    return player

def map_to_battlefield(battlefield_entity: BattlefieldEntity) -> Battlefield:
    battlefield = Battlefield(
        min_x=battlefield_entity.min_x,
        max_x=battlefield_entity.max_x,
        min_y=battlefield_entity.min_y,
        max_y=battlefield_entity.max_y,
        min_z=battlefield_entity.min_z,
        max_z=battlefield_entity.max_z
    )
    return battlefield

    

    
