import math

import game
import main
from interface import pictures, ui
from towers import projectile, tower
from interface import pictures


class SniperTower(tower.Tower):
    def __init__(self, tile):
        super().__init__(tile, 55, 6)
    
    def shoot(self):
        if self._target:
            game.GAME_INSTANCE.add_entity(SniperProjectile(self.tile.position.middle(), self._target, self._level / 2 + 1))
    
    def get_render(self, time):
        return self._add_level(SniperTower.get_img(self._aim_angle))
    
    def level_up(self):
        super().level_up()
        self._shoot_delay -= 4
    
    @staticmethod
    def get_img(aim):
        return pictures.get("sniper_tower")


class SniperProjectile(projectile.Projectile):
    def __init__(self, position, target, dmg_multiplier):
        super().__init__(position, target, 0.5, 0.1)
        self._dmg_multiplier = dmg_multiplier
    
    def hit(self):
        if not self.target_is_dead():
            self._target.damage(40 * self._dmg_multiplier, game.DAMAGE_TYPE_RAW)

            interface = ui.INTERFACE_INSTANCE
            direction = (self.target_position() - self._last_position).normalized() * 0.7
            for i in range(10):
                interface.new_smoke(self.position.to_tuple(), scale=0.1, dir_=direction.to_tuple(), speed=1, randomizer=2, lifetime=0.4, img_name=self._target.break_img)
    
    def get_render(self, time):
        angle = -(self.target_position() - self._position).angle() / math.pi * 180
        return pictures.get("dart").final_scaled(0.08).rotated(angle)
