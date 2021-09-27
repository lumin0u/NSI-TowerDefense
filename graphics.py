import math
from typing import Union, overload

import main
import board
import tiles
import pygame
from position import Position, TilePosition, Direction
import pictures
import ui

cursor_hand_reasons = {}


EMPTY_IMAGE = pygame.Surface((0, 0))


class GraphicsSettings:
	def __init__(self):
		self._zoom = 1
		self.camera_pos = Position(0, 0)
	
	@property
	def zoom(self):
		return self._zoom
	
	@zoom.setter
	def zoom(self, value):
		self._zoom = max(0.3, min(3, value))


PIXEL_PER_ZOOM = 40


def get_pixel_pos(game_pos, shift, zoom):
	return (game_pos - shift) * PIXEL_PER_ZOOM * zoom + Position(main.SCREEN_WIDTH/2, main.SCREEN_HEIGHT/2)


def get_game_pos(pixel_pos, shift, zoom):
	return (pixel_pos - Position(main.SCREEN_WIDTH/2, main.SCREEN_HEIGHT/2)) / PIXEL_PER_ZOOM / zoom + shift


def draw_image(surface: pygame.Surface, position: tuple, image: pygame.Surface, new_size: Union[tuple, pygame.rect.Rect, type(None)] = None):
	if image.get_rect().w == 0 and image.get_rect().h == 0:
		return
	if new_size is not None:
		image = pygame.transform.smoothscale(image, new_size)
		
	# n'afficher que les images qui sont visibles dans la fenetre
	if surface.get_rect().colliderect(image.get_rect().move(position)):
		surface.blit(image, position)
