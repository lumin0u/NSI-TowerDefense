import towers.tower as tower
import game
from interface import pictures

pictures.load_picture("castle", "towers/")


class Castle(tower.Tower):
    def __init__(self, tile, max_health):
        super().__init__(tile, 0)
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
        # la tour renvoie les dégats
        source.damage(amount, game.DAMAGE_TYPE_ABSOLUTE)
        
    def get_render(self, time):
        img = pictures.PICTURES["castle"].get_img(time, hash(self.tile.position))
        return img
