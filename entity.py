from abc import ABC, abstractmethod


class Entity(ABC):
    @abstractmethod
    def tick(self, current_tick):
        pass
    
    @abstractmethod
    def is_dead(self):
        pass