import game
import towers.tower as tower
from interface import pictures


class SimpleTower(tower.Tower):
    def __init__(self, tile):
        super().__init__(tile, 3, 1.8)
        self._hit_last_tick = False
        
    def tick(self, current_tick, game_):
        self._hit_last_tick = False
        super().tick(current_tick, game_)
        
    def shoot(self):
        if self._target:
            self._target.damage(1, game.DAMAGE_TYPE_RAW)
            self._hit_last_tick = True
    
    def get_render(self, time):
        img = pictures.PICTURES["simple_tower"].get_img()
        if self._hit_last_tick:
            img = img.shaded(0)
        return img
