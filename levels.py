import math
import random
from copy import copy

import main
from mobs import robuste_mob
from mobs import simple_mob
import tiles
from position import Position, TilePosition, Direction
from towers import simple_tower


class Wave:
    def __init__(self, mobs_: dict[type, int]):
        """
            mobs est un dictionnaire avec:
              pour clés les classes des mobs
              pour valeurs le nombre de ces mobs
        """
        self._remaining = mobs_.copy()
        self._mobs = mobs_
        self._scheduler = {}
        
        # start_date est exprimé en ticks
        self.start_date = 0
    
    def start(self, start_date):
        self.start_date = start_date
        buffer = copy(self._mobs)
        max_mob_count = max((v for v in self._mobs.values()))
        for mob in buffer:
            t = 0
            index = 0
            while buffer[mob] > 0:
                wait = max(2, int((math.sin(t) * 0.8 + 0.9) ** 2 * random.random() * 12 * max_mob_count / self._mobs[mob]))
                wait += random.randint(0, 4)
                wait *= main.TICK_REAL_TIME / 0.1
                if wait > 0:
                    index += wait
                    if index not in self._scheduler:
                        self._scheduler[index] = []
                    self._scheduler[index].append(mob)
                    buffer[mob] -= 1
                t += 1
    
    def is_ended(self):
        return all((v == 0 for v in self._remaining.values()))
    
    def next_mobs(self, current_tick):
        if current_tick - self.start_date in self._scheduler:
            return self._scheduler[current_tick - self.start_date]
        return []


class Level:
    def __init__(self, spawn: tiles.SpawnerTile, castle: tiles.CastleTile):
        self._spawner = spawn
        self._castle = castle
        self._tiles: list[tiles.Tile] = [self._spawner, self._castle]
        self._waves: list[Wave] = []
    
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


ALL_LEVELS = ()


def build_levels():
    global ALL_LEVELS
    level1 = Level(tiles.SpawnerTile(TilePosition(-4, 0), Direction(1, 0)), tiles.CastleTile(TilePosition(4, 0), 100))
    
    level1.tiles.append(tiles.PathTile(TilePosition(-3, 0), Direction(-1, 0), Direction(1, 0)))
    level1.tiles.append(tiles.PathTile(TilePosition(-2, 0), Direction(-1, 0), Direction(1, 0)))
    level1.tiles.append(tiles.PathTile(TilePosition(-1, 0), Direction(-1, 0), Direction(1, 0)))
    level1.tiles.append(tiles.PathTile(TilePosition(0, 0), Direction(-1, 0), Direction(1, 0)))
    level1.tiles.append(tiles.PathTile(TilePosition(1, 0), Direction(-1, 0), Direction(1, 0)))
    level1.tiles.append(tiles.PathTile(TilePosition(2, 0), Direction(-1, 0), Direction(1, 0)))
    level1.tiles.append(tiles.PathTile(TilePosition(3, 0), Direction(-1, 0), Direction(1, 0)))
    
    level1.tiles.append(tiles.BuildingTile(TilePosition(-1, 1)))
    level1.tiles.append(tiles.BuildingTile(TilePosition(0, 1)))
    level1.tiles.append(tiles.BuildingTile(TilePosition(1, 1)))
    level1.tiles.append(tiles.BuildingTile(TilePosition(-2, -1)))
    level1.tiles.append(tiles.BuildingTile(TilePosition(-1, -1)))
    level1.tiles.append(tiles.BuildingTile(TilePosition(0, -1)))
    level1.tiles.append(tiles.BuildingTile(TilePosition(2, -1)))
    
    for tile in level1.tiles:
        if type(tile) is tiles.BuildingTile:
            tile.tower = simple_tower.SimpleTower(tile)
            break
    
    level1.waves.extend([
        Wave({simple_mob.SimpleMob: 20, robuste_mob.RobusteMob: 5}),
    ])

    ALL_LEVELS = (level1, )
