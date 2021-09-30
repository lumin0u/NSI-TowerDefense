import levels
import tiles
import position
import mobs.example_mob
import random
from copy import deepcopy

DAMAGE_TYPE_RAW = 0
DAMAGE_TYPE_FIRE = 1
DAMAGE_TYPE_ICE = 2
DAMAGE_TYPE_MAGIC = 3

# ce type existe juste pour infliger des dégats fixes, indépendamment de la résistance des mobs
DAMAGE_TYPE_ABSOLUTE = 4


class Game:
    def __init__(self, level_, money):
        self._mobs = []
        self._level = level_
        self._money = money
        self._id_inc = 0
        self._wave = 0
        self._wave_obj = deepcopy(level_.waves[0])
    
    @property
    def level(self):
        return self._level
    
    def add_mob(self, mob):
        self._mobs.append(mob)
    
    def remove_mob(self, mob):
        self._mobs.remove(mob)
    
    def tick(self, current_tick):
        for mob_type in self._wave_obj.next_mobs(current_tick):
            shift = position.Position((random.random() - 0.5) * random.random(), (random.random() - 0.5) * random.random())
            self.add_mob(mob_type(self, self.level.spawner.position.middle() + shift))
        
        for mob in self.mobs:
            mob.tick()
        for tower in (tile.tower for tile in self.level.tiles if isinstance(tile, tiles.BuildingTile) and not tile.is_empty()):
            tower.tick()
        
    @property
    def mobs(self):
        return self._mobs
        
    def next_id(self):
        self._id_inc += 1
        return self._id_inc
