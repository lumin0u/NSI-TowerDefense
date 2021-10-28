import mobs.mob as mob
from entity import Entity
from abc import ABC, abstractmethod
import main
import game


class Projectile(Entity, ABC):
    def __init__(self, position, target, speed):
        """
            target est une position ou un mob
            speed est exprimé en tiles/seconde
        """
        super().__init__(game.GAME_INSTANCE, position)
        self._target = target
        self._position = position
        # l'attribut speed est, lui, exprimé en tiles/tick
        self._speed = speed * main.TICK_REAL_TIME
        self._dead = False
    
    def target_position(self):
        if isinstance(self._target, mob.Mob):
            return self._target.position
        else:
            return self._target
    
    def tick(self, current_tick, game_):
        super().tick(current_tick, game_)
        
        if isinstance(self._target, mob.Mob) and self._target.is_dead():
            self._target = self._target.position
        
        direction = self.target_position() - self._position
        
        if direction.length() < self._speed:
            self.hit()
            self._dead = True
        
        else:
            direction /= direction.length()
            self._position += direction * self._speed
    
    def is_dead(self):
        return self._dead
    
    def target_is_dead(self):
        return not isinstance(self._target, mob.Mob) or self._target.is_dead()
    
    @abstractmethod
    def hit(self):
        pass
