from abc import ABC, abstractmethod
from position import Position, TilePosition, Direction


class Tower(ABC):
	def __init__(self, tile):
		self._tile = tile
		self._target = None
	
	@abstractmethod
	def tick(self):
		pass
	
	@abstractmethod
	def get_render(self, time):
		pass
	
	@property
	def tile(self):
		return self._tile
