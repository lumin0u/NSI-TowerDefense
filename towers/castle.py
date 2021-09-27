import towers.tower
import game
import pictures
import pygame

pictures.load_picture("castle", "towers/")


class Castle(towers.tower.Tower):
	def __init__(self, tile, max_health):
		super().__init__(tile, max_health)
		
	def tick(self):
		pass
	
	def damage(self, amount: float, source):
		super().damage(amount, source)
		# la tour renvoie les dégats
		source.damage(amount, game.DAMAGE_TYPE_ABSOLUTE)
		
	def get_render(self, time):
		img = pictures.PICTURES["castle"].get_img(time, hash(self.tile.position))
		return img
