from abc import ABC, abstractmethod


class Entity(ABC):
    @abstractmethod
    def tick(self, current_tick, game_):
        pass
    
    @abstractmethod
    def is_dead(self):
        pass