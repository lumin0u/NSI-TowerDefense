import random
from copy import deepcopy

import mobs.mob as mob
import position
import tiles

DAMAGE_TYPE_RAW = 0
DAMAGE_TYPE_FIRE = 1
DAMAGE_TYPE_ICE = 2
DAMAGE_TYPE_MAGIC = 3

# ce type existe juste pour infliger des dégats fixes, indépendamment de la résistance des mobs
DAMAGE_TYPE_ABSOLUTE = 4


class Game:
    def __init__(self, level_, money):
        self._entities = []
        self._level = deepcopy(level_)
        self._money = money
        self._id_inc = 0
        self._wave = 0
    
    @property
    def level(self):
        return self._level
    
    def add_entity(self, entity):
        self._entities.append(entity)
    
    def remove_entity(self, entity):
        self._entities.remove(entity)
    
    def tick(self, current_tick):
        for mob_type in self.level.waves[self._wave].next_mobs(current_tick):
            shift = position.Position((random.random() - 0.5) * random.random() * 0.7, (random.random() - 0.5) * random.random() * 0.7)
            self.add_entity(mob_type(self, self.level.spawner.position.middle() + shift, 1))#TODO le loup 
        
        for entity in self._entities:
            if entity.is_dead():
                self.remove_entity(entity)
            else:
                entity.tick(current_tick, self)
        for tower in (tile.tower for tile in self.level.tiles if isinstance(tile, tiles.BuildingTile) and not tile.is_empty()):
            tower.tick(current_tick, self)
        
    @property
    def mobs(self):
        return [amob for amob in self._entities if isinstance(amob, mob.Mob)]
        
    def next_id(self):
        self._id_inc += 1
        return self._id_inc
