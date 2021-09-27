import board
from position import Position, TilePosition, Direction
import tiles

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
