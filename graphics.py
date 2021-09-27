import math

import board
import tiles
import pygame
from position import Position, TilePosition, Direction
import main
import pictures
import ui

cursor_hand_reasons = {}


EMPTY_IMAGE = pygame.image.frombuffer(b'', (0, 0), 'ARGB')


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


def draw_image(surface, position: tuple, image):
	if surface.get_rect().inflate(-10, -10).colliderect(image.get_rect().move(position)):
		surface.blit(image, position)
