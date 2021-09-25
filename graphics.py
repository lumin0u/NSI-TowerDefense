from game import Game
import pygame
from position import Position, TilePosition
from main import SCREEN_HEIGHT, SCREEN_WIDTH


class GraphicsSettings:
	def __init__(self):
		self.zoom = 1
		self.camera_pos = Position(0, 0)


def draw_frame(graphics_settings: GraphicsSettings, screen: pygame.Surface, game_: Game, relative_time: float):
	pygame.draw.rect(screen, (0, 0, 0), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
	
	RELATIVE_SIZE = 40 / graphics_settings.zoom
	
	for tile in game_.board.tiles:
		sreen_pos = (tile.position - graphics_settings.camera_pos) * RELATIVE_SIZE
		pygame.draw.rect(screen, (100, 200, 200), sreen_pos.to_tuple() + (RELATIVE_SIZE, RELATIVE_SIZE))
	
	pygame.display.update()
