import math
import random

import mobs.robuste_mob as robuste_mob
import mobs.simple_mob as simple_mob
import tiles
from position import Position, TilePosition, Direction


class Wave:
    def __init__(self, mobs_):
        """
            mobs est un dictionnaire avec:
              pour clés les classes des mobs
              pour valeurs le nombre de ces mobs
        """
        self._remaining = mobs_.copy()
        self._mobs = mobs_
        # start_date est exprimé en ticks
        self.start_date = 0
    
    def start(self, start_date):
        self.start_date = start_date
    
    def is_ended(self):
        return all((v == 0 for v in self._remaining.values()))
    
    def next_mobs(self, current_tick):
        to_spawn = []
        max_mob_count = max((v for v in self._mobs.values()))
        for mob_type in self._remaining:
            
            r = max_mob_count / self._mobs[mob_type] * 6 * (math.sin(current_tick / 10) + 2)
            
            if self._remaining[mob_type] > 0 and random.randint(0, max(0, int(r) + random.randint(-1, 1))) <= 0:
                to_spawn.append(mob_type)
                self._remaining[mob_type] -= 1
        return to_spawn


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
    
    level1.waves.extend([
        Wave({simple_mob.SimpleMob: 20, robuste_mob.RobusteMob: 5}),
    ])

    ALL_LEVELS = (level1, )
