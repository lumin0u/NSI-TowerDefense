import math


class Position:
	"""
		Une position définie en 2 dimensions
	"""
	def __init__(self, x, y):
		self._x = float(x)
		self._y = float(y)
	
	@property
	def x(self):
		return self._x
	
	@property
	def y(self):
		return self._y
	
	@x.setter
	def x(self, x):
		self._x = x
	
	@y.setter
	def y(self, y):
		self._y = y
	
	def __add__(self, other):
		return Position(self.x + other.x, self.y + other.y)
	
	def __sub__(self, other):
		return Position(self.x - other.x, self.y - other.y)
	
	def __mul__(self, other):
		return Position(self.x * other, self.y * other)
	
	def __truediv__(self, other):
		return Position(self.x / other, self.y / other)
	
	def __eq__(self, other):
		return self.x == other.x and self.y == other.y
	
	def __str__(self):
		return f'Position(x={self.x}, y={self.y})'
	
	def length(self):
		return math.sqrt(self.x ** 2 + self.y ** 2)
	
	def to_tuple(self):
		return self.x, self.y
	
	@staticmethod
	def of(position: tuple):
		return TilePosition(position[0], position[1])


class TilePosition(Position):
	"""
		Une position définie en 2 dimensions par x et y des entiers
	"""
	def __init__(self, x, y):
		super().__init__(x, y)
		self._x = math.floor(self._x)
		self._y = math.floor(self._y)
	
	def __str__(self):
		return f'TilePosition(x={self.x}, y={self.y})'
	
	@staticmethod
	def of(position: Position):
		return TilePosition(position.x, position.y)


class Direction(Position):
	"""
		Un vecteur en 2 dimensions
	"""
	def __str__(self):
		return f'Direction(x={self.x}, y={self.y})'
	
	@staticmethod
	def of(position: Position):
		return Direction(position.x, position.y)
