from abc import ABC, abstractmethod

import pygame

from position import TilePosition, Vector2
import towers.castle as castle
from interface import pictures, graphics


class Tile(ABC):
    """
        Classe abstraite représentant une tuile
    """
    def __init__(self, position):
        """
        :param position: TilePosition - la position de la tuile
        """
        self._position = TilePosition.of(position)
    
    @property
    def position(self):
        return self._position
    
    @abstractmethod
    def get_render(self, relative_time):
        """
            Construit et retourne le rendu de la tuile à la date time
        :param relative_time: nombre - le temps relatif au tick
        :return: MyImage - le rendu de la tuile
        """
        pass
    
    @abstractmethod
    def is_clickable(self):
        pass
    
    def get_on_screen_rect(self, interface):
        """
            Retourne le rectangle que prend l'affichage final de la tuile
        :param interface: Interface - l'instance de l'interface
        :return: Rect - le rectangle de la tuile
        """
        corner_lu = graphics.get_pixel_pos(self.position, interface)
        corner_rb = graphics.get_pixel_pos(self.position + Vector2(1, 1), interface)
        return pygame.Rect(*(corner_lu.to_tuple() + (corner_rb - corner_lu).to_tuple()))


class EmptyTile(Tile):
    """
        Représentation du vide sous forme de tuile, elle permet simplement d'éviter l'utilisation de None
    """
    def __init__(self, position: TilePosition):
        super().__init__(position)
    
    def get_render(self, relative_time):
        return pictures.MyImage.void(0, 0)
    
    def is_clickable(self):
        return False


class PathTile(Tile):
    """
        Représente une tuile de chemin
    """
    def __init__(self, position, from_, direction):
        """
        :param position: TilePosition - la position de la tuile
        :param from_: Vector2 - la direction qui pointe vers le chemin/spawner précédent
        :param direction: Vector2 - la direction qui pointe vers le chemin/tour suivant
        """
        super().__init__(position)
        
        # la direction ne peut etre que (0, 1), (0, -1), (1, 0), (-1, 0)
        assert direction.length() == 1 and (direction.x == 0 or direction.y == 0)
        if not isinstance(self, SpawnerTile):
            assert from_.length() == 1 and (from_.x == 0 or from_.y == 0)
        
        self._direction = direction
        self._from_ = from_
    
    @property
    def direction(self):
        return self._direction
    
    @property
    def from_(self):
        return self._from_

    def get_render(self, relative_time):
        # chemin droit
        if self.direction == -self._from_:
            img = pictures.get("path_WE", hash(self.position))
            if self.direction.y == 0:
                return img
            else:
                return img.rotated(90)
        # courbure de chemin
        else:
            # on calcule la rotation de l'image en fonction des tuiles suivante et précédente
            corner = self.direction + self._from_
            img = pictures.get("path_NE", hash(self.position))
            if corner == Vector2(1, -1):
                return img
            elif corner == Vector2(1, 1):
                return img.rotated(270)
            elif corner == Vector2(-1, 1):
                return img.rotated(180)
            else:
                return img.rotated(90)
    
    def is_clickable(self):
        return False


class BuildingTile(Tile):
    """
        Représente une tuile constructible, pouvant posséder une tour
    """
    def __init__(self, position):
        super().__init__(position)
        
        self._tower = None
    
    @property
    def tower(self):
        return self._tower
    
    @tower.setter
    def tower(self, value):
        self._tower = value
    
    def is_empty(self):
        return self._tower is None
    
    def get_render(self, relative_time):
        img = pictures.get("building_tile", hash(self.position))
        
        if not self.is_empty():
            img.blit(self.tower.get_render(relative_time).scaled_to(img.get_rect().size))
        return img
    
    def is_clickable(self):
        return True


class SpawnerTile(PathTile):
    """
        Représente la tuile de spawner, unique dans un niveau et faisant apparaitre les monstres
    """
    def __init__(self, position: TilePosition, direction: Vector2):
        super().__init__(position, None, direction)
    
    def get_render(self, relative_time):
        return pictures.get("spawner", hash(self.position))
    
    def is_clickable(self):
        return False


class CastleTile(BuildingTile):
    """
        Représente la tuile du chateau, unique dans un niveau et que le joueur doit défendre
    """
    def __init__(self, position: TilePosition, max_health):
        super().__init__(position)
        
        self._tower = castle.Castle(self, max_health)
