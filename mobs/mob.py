from abc import ABC, abstractmethod
from position import Position, TilePosition, Direction
from copy import copy


class Mob(ABC):
	def __init__(self, game, position: Position, attributes: dict):
		# on copie le dictionnaire pour pouvoir le modifier au besoin
		
		attributes = attributes.copy()
		
		self._game = game
		
		self._relative_position = Position(position.x % 1, position.y % 1)
		self._tile_position = TilePosition.of(position)
		self._relative_spawn_pos = copy(self._relative_position)

		self._attributes = attributes
		self._health = self.max_health
	
	@abstractmethod
	def tick(self):
		pass
	
	@property
	def max_health(self) -> float:
		return float(self._attributes["health"])
	
	@property
	def speed(self) -> float:
		"""
			la vitesse est exprimé en tuiles/ticks
		"""
		return float(self._attributes["speed"])
	
	@property
	def absolute_position(self) -> Position:
		return self._tile_position + self._relative_position
	
	@property
	def tile_position(self) -> TilePosition:
		return self._tile_position
	
	@property
	def relative_position(self) -> Position:
		return self._relative_position
	
	def advance(self):
		self.move(self._game.board.tile_at(self._tile_position).direction * self.speed)
	
	def move(self, direction: Direction):
		self.teleport(self.absolute_position + direction)
	
	def teleport(self, position: Position):
		self._relative_position = Position(position.x % 1, position.y % 1)
		self._tile_position = TilePosition.of(position)
	
	def damage(self, damage: float, type_):
		self._health -= damage / self._attributes["resistances"][type_]
