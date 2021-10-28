import math

import game
import main
import towers.tower as tower
from interface import pictures
from towers import projectile
from interface import pictures


class ExplosiveTower(tower.Tower):
	def __init__(self, tile):
		super().__init__(tile, 1, 1)  # TODO changer valeurs
	
	def shoot(self):
		if self._target:
			game.GAME_INSTANCE.add_entity(ExplosiveProjectile(self.tile.position.middle(), self._target))
	
	@staticmethod
	def get_render(time):
		img = pictures.PICTURES["explosive_tower"].get_img()
		return img


class ExplosiveProjectile(projectile.Projectile):
	def __init__(self, position, target):
		super().__init__(position, target, 1)  # TODO pas 1
	
	def hit(self):
		pass
	# TODO
	
	def get_render(self, time):
		angle = (self.target_position() - self._position).angle() / math.pi * 180 - 90
		return pictures.PICTURES["shell"].get_img().final_scaled(0.1).rotated(angle)
