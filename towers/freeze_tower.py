import random

import game
from interface import user_interface
from position import Vector2
from towers import tower
from interface import pictures


class FreezeTower(tower.Tower):
    def __init__(self, tile):
        super().__init__(tile, 59, 1.8)
        
    def shoot(self):
        if self._target:
            for i in range(70):
                interface = user_interface.INTERFACE_INSTANCE
                interface.new_smoke(self.tile.position.middle().to_tuple(), scale=0.9, dir_=(Vector2.of_angle(self._aim_angle) * (random.random()*1.5 + 0.3)).to_tuple(), randomizer=1.4, speed=10, lifetime=2, img_name="freeze")
        
        for mob in game.GAME_INSTANCE.mobs:
            if mob.position.distance(self.tile.position.middle()) < self.shoot_range:
                dmg = mob.position.distance(self.tile.position.middle()) / self.shoot_range
                mob.damage(dmg, game.DAMAGE_TYPE_ICE)
                mob.set_freeze_time(60)
        return False
    
    def get_render(self, relative_time):
        return self._add_level(FreezeTower.get_img(self._aim_angle))
    
    def level_up(self):
        super().level_up()
        self._shoot_delay -= 1
    
    @staticmethod
    def get_img(aim):
        return pictures.get("freeze_tower").smoothscaled(False)
