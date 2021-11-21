import math

import game
from interface import user_interface
from towers import projectile, tower
from interface import pictures


class SimpleTower(tower.Tower):
    def __init__(self, tile):
        super().__init__(tile, 17, 1.8)
        
    def shoot(self):
        if self._target:
            game.GAME_INSTANCE.add_entity(SimpleProjectile(self.tile.position.middle(), self._target, self._level / 2 + 1))
            return True
        return False
    
    def get_render(self, relative_time):
        return self._add_level(SimpleTower.get_img(self._aim_angle))
    
    def level_up(self):
        super().level_up()
        self._shoot_delay -= 1
    
    @staticmethod
    def get_img(aim):
        return pictures.get("simple_tower").smoothscaled(False)


class SimpleProjectile(projectile.Projectile):
    def __init__(self, position, target, dmg_multiplier):
        super().__init__(position, target, 0.175)
        self._dmg_multiplier = dmg_multiplier
        
    def hit(self):
        if not self.target_is_dead():
            self._target.damage(7 * self._dmg_multiplier, game.DAMAGE_TYPE_RAW)

            interface = user_interface.INTERFACE_INSTANCE
            direction = (self.target_position() - self._last_position).normalized() * 0.7
            for i in range(5):
                interface.new_smoke(self.position.to_tuple(), scale=0.1, dir_=direction.to_tuple(), speed=1, randomizer=2, lifetime=0.4, img_name=self._target.break_img)
    
    def get_render(self, relative_time):
        angle = -(self.target_position() - self._position).angle() / math.pi * 180
        return pictures.get("dart").final_scaled(0.1).rotated(angle)
