from position import TilePosition, Position, Direction
import abc
import towers.castle
import tiles


class Board:
	def __init__(self, spawn: tiles.SpawnerTile, castle: tiles.CastleTile):
		self._spawner = spawn
		self._castle = castle
		self._tiles = [self._spawner, self._castle]
	
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
