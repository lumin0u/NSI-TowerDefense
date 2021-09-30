import board
from position import Position, TilePosition, Direction
import tiles
import random


class Wave:
    def __init__(self, mobs):
        """
            mobs est un dictionnaire avec:
              pour clés les classes des mobs
              pour valeurs le nombre de ces mobs
        """
        self._remaining = mobs.copy()
        self._mobs = mobs
        # start_date est exprimé en ticks
        self.start_date = 0
    
    def start(self, start_date):
        self.start_date = start_date
    
    def next_mobs(self, current_tick):
        to_spawn = []
        # TODO ne pas retourner une liste vide
        return to_spawn


level1 = board.Board(tiles.SpawnerTile(TilePosition(-4, 0), Direction(1, 0)), tiles.CastleTile(TilePosition(4, 0), 100))

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

ALL_LEVELS = (level1,)
