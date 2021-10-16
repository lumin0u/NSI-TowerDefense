from abc import ABC, abstractmethod

import pygame

from position import TilePosition, Direction
import towers.castle as castle
from interface import pictures, graphics


class Tile(ABC):
    def __init__(self, position: TilePosition):
        self._position = position
    
    @property
    def position(self):
        return self._position
    
    @abstractmethod
    def get_render(self, time):
        pass
    
    @abstractmethod
    def is_clickable(self):
        pass
    
    @abstractmethod
    def onclick(self):
        pass


class EmptyTile(Tile):
    def __init__(self, position: TilePosition):
        super().__init__(position)
    
    def get_render(self, time):
        return graphics.EMPTY_IMAGE
    
    def is_clickable(self):
        return False
    
    def onclick(self):
        pass


def matches_no_order(l1, l2):
    return sorted(l1, key=hash) == sorted(l2, key=hash)


class PathTile(Tile):
    def __init__(self, position: TilePosition, from_: Direction, direction: Direction):
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

    def get_render(self, time):
        if self.direction == -self._from_:
            img = pictures.PICTURES["path_WE"].get_img(time, hash(self.position))
            if self.direction.y == 0:
                return img
            else:
                return pygame.transform.rotate(img, 90)
        else:
            l = [self.direction, self._from_]
            img = pictures.PICTURES["path_NE"].get_img(time, hash(self.position))
            if matches_no_order(l, (Direction(1, 0), Direction(0, -1))):
                return img
            elif matches_no_order(l, (Direction(1, 0), Direction(0, 1))):
                return pygame.transform.rotate(img, 270)
            elif matches_no_order(l, (Direction(-1, 0), Direction(0, 1))):
                return pygame.transform.rotate(img, 180)
            else:
                return pygame.transform.rotate(img, 90)
    
    def is_clickable(self):
        return False
    
    def onclick(self):
        pass


class BuildingTile(Tile):
    def __init__(self, position: TilePosition):
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
    
    def get_render(self, time):
        img = pictures.PICTURES["building_tile"].get_img(time, hash(self.position))
        
        if not self.is_empty():
            img.blit(self.tower.get_render(time), (0, 0))
        return img
    
    def is_clickable(self):
        return self.is_empty()
    
    def onclick(self):
        if not self.is_clickable():
            return
        # TODO show popup
        pass


class SpawnerTile(PathTile):
    def __init__(self, position: TilePosition, direction: Direction):
        super().__init__(position, Direction(0, 0), direction)
    
    def get_render(self, time):
        return pictures.PICTURES["spawner"].get_img(time, hash(self.position))
    
    def is_clickable(self):
        return False
    
    def onclick(self):
        pass


class CastleTile(BuildingTile):
    def __init__(self, position: TilePosition, max_health):
        super().__init__(position)
        
        self._tower = castle.Castle(self, max_health)
    
    def is_clickable(self):
        return False
