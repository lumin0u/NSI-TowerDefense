from abc import ABC, abstractmethod


class Entity(ABC):
    def __init__(self, game_, position):
        self._id = game_.next_id()
        
        self._position = position
        self._last_position = self._position
        self._ticks_lived = 0
    
    def tick(self, current_tick, game_):
        self._last_position = self._position
        self._ticks_lived += 1
    
    @abstractmethod
    def is_dead(self):
        pass
    
    @property
    def id_(self):
        return self._id
    
    @property
    def position(self):
        return self._position
    
    @property
    def last_position(self):
        return self._last_position
    
    @property
    def ticks_lived(self):
        return self._ticks_lived
        
    @abstractmethod
    def get_render(self, time):
        pass
