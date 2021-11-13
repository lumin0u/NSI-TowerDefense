from abc import ABC, abstractmethod

import mobs.mob as mob
from entity import Entity
import game
from interface import ui


class Projectile(Entity, ABC):
    def __init__(self, position, target, speed, magicness=0):
        """
            target est une position ou un mob
            speed est exprimé en tiles/tick
        """
        super().__init__(game.GAME_INSTANCE, position)
        self._target = target
        self._position = position
        self._speed = speed
        self._dead = False
        self._magicness = magicness
    
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
            direction = direction.normalized()
            self._position += direction * self._speed
            
            if self.tiles_travelled > 0.3:
                interface = ui.INTERFACE_INSTANCE
                smokes = int(self._speed / 0.02)
                for i in range(smokes):
                    img = "smoke"
                    interface.new_smoke((self.position - direction * self._speed * i/smokes).to_tuple(), scale=0.2, dir_=(-direction * 0.3).to_tuple(), speed=2, lifetime=0.8, img_name=img)
    
    def is_dead(self):
        return self._dead
    
    def target_is_dead(self):
        return not isinstance(self._target, mob.Mob) or self._target.is_dead()
    
    @abstractmethod
    def hit(self):
        pass
