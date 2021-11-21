import math
from abc import ABC

import pricing
import strings
import userdata
from entity import Entity
from interface import user_interface
from position import Position, Vector2
import game
import tiles


class Mob(Entity, ABC):
    def __init__(self, game_, position: Position, attributes, health, break_img):
        super().__init__(game_, position)

        # on copie le dictionnaire pour pouvoir le modifier au besoin
        attributes = attributes.copy()
        
        self._game = game_
        
        self._attributes = attributes
        self._attributes["resistances"][game.DAMAGE_TYPE_ABSOLUTE] = 1
        self._max_health = health * self._attributes["health_mul"]
        self._health = self.max_health
        self._dead = False
        self._break_img = break_img
        self._last_rotation = 0
        self._rotation = 0
        self._freeze_time = 0
    
    @property
    def max_health(self) -> float:
        return self._max_health
    
    @property
    def break_img(self):
        return self._break_img
    
    @property
    def health(self) -> float:
        return self._health
    
    @property
    def speed(self) -> float:
        """
            la vitesse est exprimé en tuiles/ticks
        """
        return float(self._attributes["speed"]) * (0.6 if self._freeze_time > 0 else 1)
    
    def tick(self, current_tick, game_):
        super().tick(current_tick, game_)
        if self._freeze_time > 0:
            self._freeze_time -= 1
        
    def advance(self):
        self._last_rotation = self._rotation
        # avancer en fonction de la direction de la tuile
        tile = self._game.level.tile_at(self._position)
        
        if isinstance(tile, tiles.PathTile):
            if tile.from_ and tile.direction != -tile.from_:
                corner = tile.position.middle() + (tile.direction + tile.from_) / 2
                corner_angle = ((tile.direction + tile.from_).angle() + 3 * math.pi / 4) % (2 * math.pi) - math.pi
                rel_pos = self.position - corner
                
                clockwise = tile.direction.angle(tile.from_) <= 0
                
                new_angle = rel_pos.angle() + (self.speed / rel_pos.length()) * (-1 if clockwise else 1)
                
                new_pos = corner + Vector2(math.cos(new_angle), math.sin(new_angle)) * rel_pos.length()
                
                self.move(new_pos - self.position)
            else:
                dir_ = tile.direction
                self.move(dir_ * self.speed)
            
        elif isinstance(tile, tiles.CastleTile):
            dmg = max(10., self.max_health / 10)
            tile.tower.damage(min(self.health, dmg) / self.max_health * self._attributes["damage"], self)
            # la tour renvoie les dégats
            self.damage(dmg, game.DAMAGE_TYPE_ABSOLUTE, earn_money=False)
            
            if self.is_dead() and userdata.TUTO_INFO["damaged"]:
                user_interface.INTERFACE_INSTANCE.popup_text = strings.get("damaged")
                userdata.TUTO_INFO["damaged"] = False
                userdata.save()
                
        self._rotation = (self.position - self.last_position).angle(invert_y=True)
    
    def move(self, direction: Vector2):
        self.teleport(self.position + direction)
    
    def teleport(self, position: Position):
        self._position = position
        
    def damage(self, damage: float, type_, earn_money=True):
        self._health -= damage / self._attributes["resistances"][type_]
        if self._health <= 0:
            self.kill(earn_money)
    
    def kill(self, earn_money):
        if earn_money:
            self._game.money += pricing.mobs_rewards[type(self)]
        self._dead = True
    
    def is_dead(self):
        return self._dead
    
    def set_freeze_time(self, time):
        self._freeze_time = time
