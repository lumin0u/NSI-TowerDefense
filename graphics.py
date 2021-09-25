import math

from game import Game
import pygame
from position import Position, TilePosition
from main import SCREEN_HEIGHT, SCREEN_WIDTH


class GraphicsSettings:
	def __init__(self):
		self._zoom = 1
		self.camera_pos = Position(0, 0)
	
	@property
	def zoom(self):
		return self._zoom
	
	@zoom.setter
	def zoom(self, value):
		self._zoom = max(0.1, min(5, value))


def get_pixel_pos(game_pos, shift, zoom):
	return (game_pos - shift) * 40 * zoom + Position(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)


def get_game_pos(pixel_pos, shift, zoom):
	return (pixel_pos - Position(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)) / 40 / zoom + shift


last_zoom = 1 / 100
last_position = Position(0, 0)


def draw_frame(graphics_settings: GraphicsSettings, screen: pygame.Surface, game_: Game, time, last_frame):
	pygame.draw.rect(screen, (0, 0, 0), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
	
	global last_zoom
	delay = max(0.01, time - last_frame)
	last_zoom = graphics_settings.zoom if 0.0005/delay > 1 else last_zoom * (1 - 0.0005/delay) + graphics_settings.zoom * 0.0005/delay
	
	global last_position
	delay = max(0.01, time - last_frame)
	last_position = graphics_settings.camera_pos if 0.0005/delay > 1 else last_position * (1 - 0.0005/delay) + graphics_settings.camera_pos * 0.0005/delay
	
	RELATIVE_SIZE = 40 * last_zoom
	
	for tile in game_.board.tiles:
		screen_pos = (Position.of(tile.position) - last_position) * RELATIVE_SIZE
		screen_pos += Position(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
		pygame.draw.rect(screen, (100, 200, 200), screen_pos.to_tuple() + (RELATIVE_SIZE, RELATIVE_SIZE))
	
	pygame.display.update()
