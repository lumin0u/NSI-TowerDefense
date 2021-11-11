import math

import game
import main
import towers.tower as tower
from interface import pictures, ui
from towers import projectile
from interface import pictures


class ExplosiveTower(tower.Tower):
    def __init__(self, tile):
        super().__init__(tile, 60, 2.3)
    
    def shoot(self):
        if self._target:
            game.GAME_INSTANCE.add_entity(ExplosiveProjectile(self.tile.position.middle(), self._target, self._level / 2 + 1))
    
    def get_render(self, time):
        return self._add_level(ExplosiveTower.get_img(self._aim_angle))
    
    def level_up(self):
        super().level_up()
        self._shoot_delay -= 4
    
    @staticmethod
    def get_img(aim):
        return pictures.get("explosive_tower").smoothscaled(False)


class ExplosiveProjectile(projectile.Projectile):
    def __init__(self, position, target, dmg_multiplier):
        super().__init__(position, target, 0.1)
        self._dmg_multiplier = dmg_multiplier
    
    def hit(self):
        for mob in game.GAME_INSTANCE.mobs:
            if self.target_position().distance(mob.position) < 1:
                dmg = (1 - self.target_position().distance(mob.position)) / 1
                mob.damage((dmg * self._dmg_multiplier) * 5, game.DAMAGE_TYPE_RAW)
                mob.damage((dmg * self._dmg_multiplier) * 9, game.DAMAGE_TYPE_FIRE)
        
        interface = ui.INTERFACE_INSTANCE
        interface.new_smoke(self.position.to_tuple(), scale=1, dir_=0, speed=1, lifetime=0.4, img_name="explosion")
    
    def get_render(self, time):
        angle = -(self.target_position() - self._position).angle() / math.pi * 180
        return pictures.get("shell").final_scaled(0.1).rotated(angle)
