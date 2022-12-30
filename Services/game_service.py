from dao.game_dao import GameDao, BattlefieldEntity, PlayerEntity, map_to_game
from model.game import Game
from model.battlefield import Battlefield
from model.player import Player
from model.vessel import Vessel

class GameService:
    def __init__(self):
        self.game_dao = GameDao()

    def create_game(self, player_name: str, min_x: int, max_x: int, min_y: int, max_y: int, min_z: int, max_z: int) -> int:
        game = Game()
        battle_field = Battlefield(min_x, max_x, min_y, max_y, min_z, max_z)
        game.add_player(Player(player_name, battle_field))
        return self.game_dao.create_game(game)

    def join_game(self, game_id: int, player_name: str) -> bool:
        game = self.game_dao.find_game(game_id)
        if game is None:
            return False
        if len(game.get_players()) >= 2:
            return False
        game.add_player(Player(player_name))
        self.game_dao.update_game(game)
        return True 
    
    def  get_game(self, game_id: int) -> Game:
        game_entity = self.game_dao.find_game(game_id)
        if game_entity is None:
            return None
        game = map_to_game(game_entity)
        return game
    
    def add_vessel(self, game_id: int, player_name: str, vessel_type: str, x: int, y: int, z: int) -> bool:
        game = self.game_dao.find_game(game_id)
        if game is None:
            return False
        player = next((player for player in game.get_players() if player.name == player_name), None)
        if player is None:
            return False
        battlefield = player.battle_field
        if not battlefield.is_valid_position(x, y, z):
            return False
        vessel = Vessel(vessel_type, x, y, z)
        battlefield.add_vessel(vessel)
        self.game_dao.update_game(game)
        return True
    
    def shoot_at(self, game_id: int, shooter_name: str, vessel_id: int, x: int, y: int, z: int) -> bool:
        game = self.game_dao.find_game(game_id)
        if game is None:
            return False
        shooter = next((player for player in game.get_players() if player.name == shooter_name), None)
        if shooter is None:
            return False
        battlefield = shooter.battle_field
        vessel = battlefield.find_vessel(vessel_id)
        if vessel is None:
            return False
        if not battlefield.is_valid_position(x, y, z):
            return False
        if not vessel.can_shoot_at(x, y, z):
            return False
        battlefield.shoot_at(x, y, z)
        self.game_dao.update_game(game)
        return True
    
    def get_game_status(self, game_id: int, shooter_name: str) -> str:
        game = self.game_dao.find_game(game_id)
        if game is None:
            return "ENCORS"
        shooter = next((player for player in game.get_players() if player.name == shooter_name), None)
        if shooter is None:
            return "ENCORS"
        battlefield = shooter.battle_field
        if battlefield.has_won():
            return "GAGNE"
        elif battlefield.has_lost():
            return "PERDU"
        else:
            return "ENCORS"


    