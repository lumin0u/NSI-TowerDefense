from board import Board
from mobs.mob import Mob

DAMAGE_TYPE_RAW = 0
DAMAGE_TYPE_FIRE = 1
DAMAGE_TYPE_ICE = 2
DAMAGE_TYPE_MAGIC = 3

# ce type existe juste pour infliger des dégats fixes, indépendamment de la résistance des mobs
DAMAGE_TYPE_ABSOLUTE = 4


class Game:
	def __init__(self, board: Board):
		self._mobs = []
		self._board = board
	
	@property
	def board(self):
		return self._board
	
	def add_mob(self, mob: Mob):
		self._mobs.append(mob)
	
	def remove_mob(self, mob: Mob):
		self._mobs.remove(mob)
