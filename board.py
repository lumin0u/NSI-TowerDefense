from position import TilePosition, Position, Direction
from abc import ABC, abstractmethod
from towers.castle import Castle


class Board:
	def __init__(self, spawn: TilePosition, castle: TilePosition):
		self._spawner = SpawnerTile(spawn)
		self._castle = CastleTile(castle, 100)
		self._tiles = [self._spawner, self._castle]
	
	def tile_at(self, position: Position):
		# on recherche dans nos tuiles s'il en existe une a cette position
		for tile in self._tiles:
			if tile.position == TilePosition.of(position):
				return tile
		
		# s'il n'en existe pas, on en créé une vide
		return EmptyTile(TilePosition.of(position))
	
	@property
	def tiles(self):
		return self._tiles


class Tile(ABC):
	def __init__(self, position: TilePosition):
		self._position = position
	
	@property
	def position(self):
		return self._position


class EmptyTile(Tile):
	def __init__(self, position: TilePosition):
		super().__init__(position)


class PathTile(Tile):
	def __init__(self, position: TilePosition, direction: Direction):
		super().__init__(position)
		
		# la direction ne peut etre que (0, 1), (0, -1), (1, 0), (-1, 0)
		assert direction.length() == 1 and (direction.x == 0 or direction.y == 0)
		self._direction = direction
	
	@property
	def direction(self):
		return self._direction


class BuildingTile(Tile):
	def __init__(self, position: TilePosition):
		super().__init__(position)
		
		self._tower = None
	
	@property
	def tower(self):
		return self._tower
	
	def is_empty(self):
		return self._tower is None


class SpawnerTile(Tile):
	def __init__(self, position: TilePosition):
		super().__init__(position)


class CastleTile(BuildingTile):
	def __init__(self, position: TilePosition, max_health):
		super().__init__(position)
		
		self._tower = Castle(self, max_health)
