import math
import random
from copy import copy

import main
from mobs import robuste_mob, boss_mob
from mobs import simple_mob
import tiles
from position import Position, TilePosition, Direction
from towers import simple_tower


class Wave:
    def __init__(self, preparation, mobs_, boss_health=0):
        """
            mobs est un dictionnaire avec:
              pour clés les classes des mobs
              pour valeurs le nombre de ces mobs
        """
        self._preparation = preparation
        self._mobs = mobs_
        self._scheduler = {}
        
        # start_date est exprimé en ticks
        self.start_date = 0
        self._boss_health = boss_health
    
    @property
    def preparation(self):
        return self._preparation
    
    @property
    def boss_health(self):
        return self._boss_health
    
    def start(self, start_date):
        self._scheduler = {}
        self.start_date = start_date
        buffer = copy(self._mobs)
        max_mob_count = max((v for v in self._mobs.values()))
        for mob in buffer:
            t = 0
            index = 0
            while buffer[mob] > 0:
                r1 = 2
                r2 = (math.sin(t) * 0.8 + 0.9) ** 2
                r3 = max_mob_count / self._mobs[mob]
                
                wait = max(2, int(random.random() * 12 * r1 * r2 * r3))
                wait += random.randint(0, 4)
                
                if wait > 0:
                    index += wait
                    if index not in self._scheduler:
                        self._scheduler[index] = []
                    self._scheduler[index].append(mob)
                    buffer[mob] -= 1
                t += 1
    
    def is_ended(self, current_tick):
        return not any((k > current_tick - self.start_date for k in self._scheduler))
    
    def next_mobs(self, current_tick):
        if current_tick - self.start_date in self._scheduler:
            return self._scheduler[current_tick - self.start_date]
        return []


class Level:
    def __init__(self, spawn: tiles.SpawnerTile, castle: tiles.CastleTile, money, tiles_, waves, available_towers):
        self._spawner = spawn
        self._castle = castle
        self._tiles: list[tiles.Tile] = [self._spawner, self._castle] + tiles_.copy()
        self._waves: list[Wave] = waves.copy()
        self._money = money
        self._available_towers = available_towers
    
    def tile_at(self, position: Position):
        # on recherche dans nos tuiles s'il en existe une a cette position
        for tile in self._tiles:
            if tile.position == TilePosition.of(position):
                return tile
        
        # s'il n'en existe pas, on en créé une vide
        return tiles.EmptyTile(TilePosition.of(position))
    
    @property
    def tiles(self):
        return self._tiles
    
    @property
    def waves(self) -> list:
        return self._waves
    
    @property
    def spawner(self):
        return self._spawner
    
    @property
    def castle(self):
        return self._castle
    
    @property
    def money(self):
        return self._money
    
    @property
    def available_towers(self):
        return self._available_towers


ALL_LEVELS = ()


def cardinal_to_direction(s):
    return {"S": Direction(0, 1), "N": Direction(0, -1), "E": Direction(1, 0), "W": Direction(-1, 0)}[s]


# pour avoir un nom plus court
ctd = cardinal_to_direction


def build_levels():
    global ALL_LEVELS
    
    mobs_names = {
        "simple": simple_mob.SimpleMob,
        "robuste": robuste_mob.RobusteMob,
        "boss": boss_mob.BossMob,
        "air": None
    }
    
    levels_json = eval(open("levels/levels.json", mode="r").read())
    
    levels_list = []
    
    for level_file in levels_json:
        level = eval(open("levels/" + level_file, mode="r").read())
        
        path_current = TilePosition.of(level["spawner"])
        
        spawner = tiles.SpawnerTile(path_current, ctd(level["path"][0]))
        tiles_ = []
        
        for i in range(len(level["path"]) - 1):
            path_current += ctd(level["path"][i])
            tiles_.append(tiles.PathTile(path_current, -ctd(level["path"][i]), ctd(level["path"][i + 1])))
            
        path_current += ctd(level["path"][-1])
        castle = tiles.CastleTile(path_current, level["castle_health"])
        
        money = level["money"]
        
        for tower_slot in level["tower_slots"]:
            tiles_.append(tiles.BuildingTile(TilePosition.of(tower_slot)))
        
        waves = []
        
        for wave in level["waves"]:
            waves.append(Wave(wave["preparation"], {mobs_names[k]: v for k, v in wave["mobs"].items()}, wave["boss_health"] if "boss_health" in wave else 0))
        
        levels_list.append(Level(spawner, castle, money, tiles_, waves))
    
    ALL_LEVELS = tuple(levels_list)
