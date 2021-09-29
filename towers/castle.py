import towers.tower
import game
import pictures
import pygame

pictures.load_picture("castle", "towers/")


class Castle(towers.tower.Tower):
	def __init__(self, tile, max_health):
		super().__init__(tile)
		self._max_health = max_health
		self._health = float(max_health)
		
	def tick(self):
		pass
	
	@property
	def max_health(self):
		return self._max_health

	@property
	def health(self):
		return self._health
	
	def damage(self, amount: float, source):
		self._health -= amount
		# la tour renvoie les dégats
		source.damage(amount, game.DAMAGE_TYPE_ABSOLUTE)
		
	def get_render(self, time):
		img = pictures.PICTURES["castle"].get_img(time, hash(self.tile.position))
		return img
