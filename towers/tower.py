from abc import ABC, abstractmethod

import pygame

from interface import pictures, graphics
from position import Position, TilePosition, Direction
import game


class Tower(ABC):
    def __init__(self, tile, shoot_delay, shoot_range):
        self._tile = tile
        self._target = None
        self._shoot_delay = shoot_delay
        self._last_shot = 0
        self._shoot_range = shoot_range
        self._level = 0
    
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
            for mob in sorted(game_.mobs, key=lambda m: m.ticks_lived, reverse=False):
                if mob.position.distance(self._tile.position.middle()) <= self._shoot_range:
                    self._target = mob
    
    @abstractmethod
    def shoot(self):
        pass
    
    @abstractmethod
    def get_render(self, time):
        pass
    
    def _add_level(self, img: pictures.MyImage):
        # if self._level > 0:
        level_img = pygame.Surface((img.get_width() // 10, img.get_height() // 10))
        level_img.blit(graphics.TOWER_LVL_FONT.render(str(self._level + 1), True, (0, 200, 0)), (0, 0))
        img.blit(graphics.TOWER_LVL_FONT.render(str(self._level + 1), True, (0, 200, 0)), (0, 0))
        return img
    
    @property
    def tile(self):
        return self._tile
