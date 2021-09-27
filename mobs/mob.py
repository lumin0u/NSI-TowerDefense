from abc import ABC, abstractmethod
from position import Position, TilePosition, Direction
from copy import copy
import random
import game


class Mob(ABC):
	def __init__(self, game_, position: Position, attributes: dict):
		# on copie le dictionnaire pour pouvoir le modifier au besoin
		
		attributes = attributes.copy()
		
		self._game = game_
		
		self._position = position
		# TODO: stockage de la position relative a la tuile
		
		self._attributes = attributes
		self._attributes["resistances"][game.DAMAGE_TYPE_ABSOLUTE] = 1
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
	def position(self) -> Position:
		return self._position
	
	def advance(self):
		# TODO avancer en fonction de la direction de la tuile
		pass
	
	def move(self, direction: Direction):
		self.teleport(self.position + direction)
	
	def teleport(self, position: Position):
		# TODO
		pass
	
	def damage(self, damage: float, type_):
		self._health -= damage / self._attributes["resistances"][type_]
		
	@abstractmethod
	def get_render(self, time):
		pass
	
