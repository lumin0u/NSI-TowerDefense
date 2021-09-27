import board
import tiles
import position
import mobs.example_mob

DAMAGE_TYPE_RAW = 0
DAMAGE_TYPE_FIRE = 1
DAMAGE_TYPE_ICE = 2
DAMAGE_TYPE_MAGIC = 3

# ce type existe juste pour infliger des dégats fixes, indépendamment de la résistance des mobs
DAMAGE_TYPE_ABSOLUTE = 4


class Game:
	def __init__(self, board_, money):
		self._mobs = []
		self._board = board_
		self._money = money
		
		self.add_mob(mobs.example_mob.ExampleMob(self, position.Position(5, 5)))
	
	@property
	def board(self):
		return self._board
	
	def add_mob(self, mob):
		self._mobs.append(mob)
	
	def remove_mob(self, mob):
		self._mobs.remove(mob)
	
	def tick(self):
		for mob in self.mobs:
			mob.tick()
		for tower in (tile.tower for tile in self.board.tiles if isinstance(tile, tiles.BuildingTile) and not tile.is_empty()):
			tower.tick()
		
	@property
	def mobs(self):
		return self._mobs
