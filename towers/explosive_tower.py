import math

import game
import main
import towers.tower as tower
from interface import pictures
from towers import projectile
from interface import pictures


class ExplosiveTower(tower.Tower):
	def __init__(self, tile):
		super().__init__(tile, 30, 2.3)
	
	def shoot(self):
		if self._target:
			game.GAME_INSTANCE.add_entity(ExplosiveProjectile(self.tile.position.middle(), self._target, self._level + 1))
	
	def get_render(self, time):
		return self._add_level(pictures.PICTURES["explosive_tower"].get_img())


class ExplosiveProjectile(projectile.Projectile):
	def __init__(self, position, target, dmg_multiplier):
		super().__init__(position, target, 0.1)
		self._dmg_multiplier = dmg_multiplier
	
	def hit(self):
		for mob in game.GAME_INSTANCE.mobs:
			if self.target_position().distance(mob.position) < 1:
				dmg = (1 - self.target_position().distance(mob.position)) / 1
				mob.damage((dmg * self._dmg_multiplier) * 3, game.DAMAGE_TYPE_RAW)
				mob.damage((dmg * self._dmg_multiplier) * 4, game.DAMAGE_TYPE_FIRE)
	
	def get_render(self, time):
		angle = -(self.target_position() - self._position).angle() / math.pi * 180
		return pictures.PICTURES["shell"].get_img().final_scaled(0.1).rotated(angle)
