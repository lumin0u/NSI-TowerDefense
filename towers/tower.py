from abc import ABC, abstractmethod

import pygame.examples.aliens

from position import TilePosition, Position, Direction
from mobs.mob import Mob

class Tower(ABC):
	def __init__(self, tile, max_health):
		self._tile = tile
		self._max_health = max_health
		self._health = float(max_health)
		self._target: Mob = None
	
	@abstractmethod
	def tick(self):
		pass
	
	@property
	def max_health(self):
		return self._max_health

	@property
	def health(self):
		return self._health
	
	def damage(self, amount: float, source: Mob):
		self._health -= amount
