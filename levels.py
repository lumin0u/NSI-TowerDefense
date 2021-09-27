import board
from position import TilePosition, Direction

level1 = board.Board(board.SpawnerTile(TilePosition(-4, 0), Direction(1, 0)), board.CastleTile(TilePosition(4, 0), 100))

level1.tiles.append(board.PathTile(TilePosition(-3, 0), Direction(-1, 0), Direction(1, 0)))
level1.tiles.append(board.PathTile(TilePosition(-2, 0), Direction(-1, 0), Direction(1, 0)))
level1.tiles.append(board.PathTile(TilePosition(-1, 0), Direction(-1, 0), Direction(1, 0)))
level1.tiles.append(board.PathTile(TilePosition(0, 0), Direction(-1, 0), Direction(1, 0)))
level1.tiles.append(board.PathTile(TilePosition(1, 0), Direction(-1, 0), Direction(1, 0)))
level1.tiles.append(board.PathTile(TilePosition(2, 0), Direction(-1, 0), Direction(1, 0)))
level1.tiles.append(board.PathTile(TilePosition(3, 0), Direction(-1, 0), Direction(1, 0)))

level1.tiles.append(board.BuildingTile(TilePosition(-1, 1)))
level1.tiles.append(board.BuildingTile(TilePosition(0, 1)))
level1.tiles.append(board.BuildingTile(TilePosition(1, 1)))
level1.tiles.append(board.BuildingTile(TilePosition(-2, -1)))
level1.tiles.append(board.BuildingTile(TilePosition(-1, -1)))
level1.tiles.append(board.BuildingTile(TilePosition(0, -1)))
level1.tiles.append(board.BuildingTile(TilePosition(2, -1)))

all_levels = [level1]
