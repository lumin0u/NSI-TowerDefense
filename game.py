import board
import mobs.mob

DAMAGE_TYPE_RAW = 0
DAMAGE_TYPE_FIRE = 1
DAMAGE_TYPE_ICE = 2
DAMAGE_TYPE_MAGIC = 3

# ce type existe juste pour infliger des dégats fixes, indépendamment de la résistance des mobs
DAMAGE_TYPE_ABSOLUTE = 4


class Game:
	def __init__(self, board_):
		self._mobs = []
		self._board = board_
		self._money = 200
	
	@property
	def board(self):
		return self._board
	
	def add_mob(self, mob):
		self._mobs.append(mob)
	
	def remove_mob(self, mob):
		self._mobs.remove(mob)
		
	@property
	def mobs(self):
		return self._mobs
