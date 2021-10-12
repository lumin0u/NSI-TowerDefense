from abc import ABC, abstractmethod
from position import Position, TilePosition, Direction


class Tower(ABC):
    def __init__(self, tile, shoot_delay):
        self._tile = tile
        self._target = None
        self._shoot_delay = shoot_delay
        self._last_shot = 0
    
    def tick(self, current_tick):
        if current_tick - self._last_shot > self._shoot_delay:
            if self._target is not None:
                self.shoot()
                self._last_shot = self._current_tick
        
    
    @abstractmethod
    def shoot(self):
        pass
    
    @abstractmethod
    def get_render(self, time):
        pass
    
    @property
    def tile(self):
        return self._tile

