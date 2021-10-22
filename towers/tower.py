from abc import ABC, abstractmethod
from position import Position, TilePosition, Direction
import game


class Tower(ABC):
    def __init__(self, tile, shoot_delay, shoot_range):
        self._tile = tile
        self._target = None
        self._shoot_delay = shoot_delay
        self._last_shot = 0
        self._shoot_range = shoot_range
    
    def tick(self, current_tick, game_):
        if current_tick - self._last_shot > self._shoot_delay:
            if self._target is not None:
                self.shoot()
                self._last_shot = current_tick
                
        # on change de target s'il est trop loin ou mort
        if self._target is not None and (self._target.is_dead() or self._target.position.distance(self._tile.position.middle()) > self._shoot_range):
            self._target = None
        
        # et on ne change pas sinon
        if self._target is None:
            for mob in game_.mobs:
                if mob.position.distance(self._tile.position.middle()) <= self._shoot_range:
                    self._target = mob
    
    @abstractmethod
    def shoot(self):
        pass
    
    @abstractmethod
    def get_render(self, time):
        pass
    
    @property
    def tile(self):
        return self._tile
