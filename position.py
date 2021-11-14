import math


class Position:
	"""
		Une position immutable définie en 2 dimensions dans un plan cartésien
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
	
	def length(self):
		"""
			Retourne la distance de cette position au point (0, 0)
			Permet, dans le cas d'un vecteur, de retourner sa longueur, d'où le nom de cette méthode
		:return: nombre - la distance au point (0, 0)
		"""
		return math.sqrt(self.x ** 2 + self.y ** 2)
	
	def to_tuple(self):
		"""
		:return: tuple - (x, y)
		"""
		return self.x, self.y
	
	def distance(self, other):
		"""
			Retourne la distance entre cette position et la position other
		:param other: Position - une autre position
		:return: nombre - la distance à other
		"""
		return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
	
	def normalized(self):
		"""
			Cette méthode s'applique aux vecteurs mais a les mêmes effets sur une position.
			Retourne le vecteur unitaire de même direction
		:return: Vector2 - le vecteur normalisée
		"""
		return Vector2.of(self) / self.length()
	
	def angle(self, other=None):
		"""
			Cette méthode s'applique aux vecteurs mais a les mêmes effets sur une position.
			Retourne l'angle formé entre ce vecteur et le vecteur other, ou le vecteur (1, 0) si indéfini.
			L'angle est exprimé en radians
		:param other: Vector2 | None - un autre vecteur
		:return: nombre - l'angle formé en radians
		"""
		if other:
			return (self.angle() - other.angle()) % (2 * math.pi) - math.pi
		else:
			return math.atan2(self._y, self._x)
	
	@staticmethod
	def of(position):
		"""
			Retourne une nouvelle position à partir de l'objet donné
		:param position: tuple | list | Position - tuple (x, y), liste [x, y] ou Position
		:return: Position - la position créée
		"""
		if isinstance(position, tuple) or isinstance(position, list):
			return Position(position[0], position[1])
		elif isinstance(position, Position):
			return Position(position.x, position.y)
	
	# les méthodes suivantes sont des surcharges d'opérateurs
	
	def __add__(self, other):
		if not isinstance(other, Position):
			raise TypeError()
		return self.__class__(self.x + other.x, self.y + other.y)
	
	def __sub__(self, other):
		if not isinstance(other, Position):
			raise TypeError()
		return self.__class__(self.x - other.x, self.y - other.y)
	
	def __mul__(self, other):
		if type(other) is not int and type(other) is not float:
			raise TypeError()
		return self.__class__(self.x * other, self.y * other)
	
	def __truediv__(self, other):
		if type(other) is not int and type(other) is not float:
			raise TypeError()
		return self.__class__(self.x / other, self.y / other)
	
	def __eq__(self, other):
		if not isinstance(other, Position):
			return False
		return self.x == other.x and self.y == other.y
	
	def __str__(self):
		return f'Position(x={self.x}, y={self.y})'
	
	def __neg__(self):
		return self.__class__(-self.x, -self.y)
	
	def __hash__(self):
		return hash(self.x * 86281339878799307 + 7 * 8628133987879930 * self.y)


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
	
	def middle(self):
		"""
			Retourne la position représentant le centre de la tuile
		:return: Position - le centre de la tuile
		"""
		return Position(self.x + 0.5, self.y + 0.5)
	
	@staticmethod
	def of(position):
		"""
			Retourne une nouvelle position à partir de l'objet donné
		:param position: tuple | list | Position - tuple (x, y), liste [x, y] ou Position
		:return: Position - la position créée
		"""
		if isinstance(position, tuple) or isinstance(position, list):
			return TilePosition(position[0], position[1])
		elif isinstance(position, Position):
			return TilePosition(position.x, position.y)
	
	def __add__(self, other):
		if isinstance(other, Position) and type(other) is not TilePosition:
			return Position(self.x + other.x, self.y + other.y)
		return super().__add__(other)
	
	def __sub__(self, other):
		if isinstance(other, Position) and type(other) is not TilePosition:
			return Position(self.x - other.x, self.y - other.y)
		return super().__sub__(other)


class Vector2(Position):
	"""
		Un vecteur en 2 dimensions
	"""
	def __str__(self):
		return f'Vector(x={self.x}, y={self.y})'
	
	@staticmethod
	def of(position):
		"""
			Retourne une nouvelle position à partir de l'objet donné
		:param position: tuple | list | Position - tuple (x, y), liste [x, y] ou Position
		:return: Position - la position créée
		"""
		if isinstance(position, tuple) or isinstance(position, list):
			return Vector2(*position)
		elif isinstance(position, Position):
			return Vector2(position.x, position.y)
	
	@staticmethod
	def of_angle(angle):
		"""
			Retourne le vecteur unitaire ayant 'angle' pour angle au vecteur (1, 0)
		:param angle: nombre - l'angle du vecteur en radians
		:return: Vector2 - le vecteur unitaire
		"""
		return Vector2(math.cos(angle), math.sin(angle))
