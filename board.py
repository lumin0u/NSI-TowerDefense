from position import TilePosition, Position, Direction
from abc import ABC, abstractmethod
from towers.castle import Castle
from tiles import PathTile, Tile, EmptyTile, SpawnerTile, BuildingTile, CastleTile


class Board:
	def __init__(self, spawn: SpawnerTile, castle: CastleTile):
		self._spawner = spawn
		self._castle = castle
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
