from towers.tower import Tower
from mobs.mob import Mob
import game


class Castle(Tower):
	def __init__(self, tile, max_health):
		super().__init__(tile, max_health)
		
	def tick(self):
		pass
	
	def damage(self, amount: float, source: Mob):
		super().damage(amount, source)
		# la tour renvoie les dégats
		source.damage(amount, game.DAMAGE_TYPE_ABSOLUTE)
