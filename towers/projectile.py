import mobs.mob as mob
from entity import Entity
from abc import ABC, abstractmethod


class Projectile(Entity, ABC):
    def __init__(self, position, target, speed):
        """
            target est une position ou un mob
            speed est exprimé en tiles/tick
        """
        self._target = target
        self._position = position
        self._speed = speed
        self._dead = False
    
    def target_position(self):
        if isinstance(self._target, mob.Mob):
            return self._target.position
        else:
            return self._target
    
    def tick(self, current_tick):
        if isinstance(self._target, Mob) and self._target.is_dead():
            self._target = self._target.position
        
        direction = self.target_position() - self._position
        
        if direction.length() < self.speed:
            self.hit()
            self._dead = True
        
        else:
            direction /= direction.length()
            self._position += direction
    
    def is_dead(self):
        return self._dead
    
    @abstractmethod
    def hit(self):
        pass
