import towers.tower as tower
import game
from interface import pictures


class Castle(tower.Tower):
    def __init__(self, tile, max_health):
        super().__init__(tile, 0, 0)
        self._max_health = max_health
        self._health = float(max_health)
        
    def shoot(self):
        pass
    
    @property
    def max_health(self):
        return self._max_health

    @property
    def health(self):
        return self._health
    
    def damage(self, amount: float, source):
        self._health -= amount
        
    def get_render(self, time):
        img = pictures.PICTURES["castle"].get_img(hash(self.tile.position))
        return img
