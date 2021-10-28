import math

import game
import main
import towers.tower as tower
from interface import pictures
from towers import projectile
from interface import pictures


class SimpleTower(tower.Tower):
    def __init__(self, tile):
        super().__init__(tile, 0.5 / main.TICK_REAL_TIME, 1.8)
        
    def shoot(self):
        if self._target:
            game.GAME_INSTANCE.add_entity(SimpleProjectile(self.tile.position.middle(), self._target))
    
    @staticmethod
    def get_render(time):
        img = pictures.PICTURES["simple_tower"].get_img()
        return img


class SimpleProjectile(projectile.Projectile):
    def __init__(self, position, target):
        super().__init__(position, target, 3.5)
        
    def hit(self):
        if not self.target_is_dead():
            self._target.damage(7, game.DAMAGE_TYPE_RAW)
    
    def get_render(self, time):
        angle = (self.target_position() - self._position).angle() / math.pi * 180 - 90
        return pictures.PICTURES["dart"].get_img().final_scaled(0.1).rotated(angle)
