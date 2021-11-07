from abc import ABC, abstractmethod

import pygame

import pricing
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
        self._aim_angle = 0
    
    def tick(self, current_tick, game_):
        if self._target:
            self._aim_angle = (self._target.position - self._tile.position.middle()).angle()
        
        # on reset le target s'il est trop loin ou mort
        if self._target and (self._target.is_dead() or self._target.position.distance(self._tile.position.middle()) > self._shoot_range):
            self._target = None
        
        # et on en choisit un nouveau si besoin
        if self._target is None:
            for mob in sorted(game_.mobs, key=lambda m: m.ticks_lived, reverse=False):
                if mob.position.distance(self._tile.position.middle()) <= self._shoot_range:
                    self._target = mob
        
        if current_tick - self._last_shot > self._shoot_delay:
            if self._target is not None:
                self.shoot()
                self._last_shot = current_tick
    
    @abstractmethod
    def shoot(self):
        pass
    
    @abstractmethod
    def get_render(self, time):
        pass
    
    def _add_level(self, img: pictures.MyImage):
        # if self._level > 0:
        level_img = pictures.MyImage(graphics.TOWER_LVL_FONT.render(str(self._level + 1), True, (0, 200, 0)))
        img.blit(level_img.scaled(img.get_width() / 64), (0, 0))
        return img
    
    @property
    def tile(self):
        return self._tile
    
    def has_next_level(self):
        return self._level + 1 < len(pricing.get_tower_level_prices(self.__class__))
    
    def get_next_level_price(self):
        return pricing.get_tower_level_prices(self.__class__)[self._level + 1]
    
    def level_up(self):
        self._level += 1
