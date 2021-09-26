import math

import board
import tiles
from game import Game
import pygame
from position import Position, TilePosition
import main
from pictures import PICTURES
from pygame import gfxdraw

cursor_hand_reasons = {}


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


DEFAULT_HALF_STATE = {"zoom": 1 / 100, "camera_pos": Position(0, 0)}


def draw_frame(half_state, graphics_settings: GraphicsSettings, screen: pygame.Surface, game_: Game, time, last_frame):
	pygame.draw.rect(screen, (0, 0, 0), (0, 0, main.SCREEN_WIDTH, main.SCREEN_HEIGHT))
	
	delay = max(0.01, time - last_frame)
	half_movement = min(1., 1 / 2000 / delay)
	
	half_state["zoom"] = half_state["zoom"] * (1 - half_movement) + graphics_settings.zoom * half_movement
	
	half_state["camera_pos"] = half_state["camera_pos"] * (1 - half_movement) + graphics_settings.camera_pos * half_movement
	
	RELATIVE_SIZE = PIXEL_PER_ZOOM * half_state["zoom"]
	
	for tile in game_.board.tiles:
		# concatenation de (cornerX, cornerY) et de (width, height)
		corner_draw = get_pixel_pos(tile.position, half_state["camera_pos"], half_state["zoom"]).to_tuple()
		img_new_size = (math.ceil(RELATIVE_SIZE), math.ceil(RELATIVE_SIZE))
		rect = corner_draw + img_new_size
		
		img = tile.get_render(time)
		screen.blit(pygame.transform.smoothscale(img, img_new_size), corner_draw)
		
		if isinstance(tile, tiles.BuildingTile) and tile.is_empty():
			if pygame.rect.Rect(rect).collidepoint(pygame.mouse.get_pos()):
				main.set_hand_reason("hover_building_"+str(hash(tile.position)), True)
				screen.blit(pygame.transform.smoothscale(PICTURES["mouse_hover"].get_img(time, None), img_new_size), corner_draw)
			else:
				main.set_hand_reason("hover_building_"+str(hash(tile.position)), False)
	
	pygame.display.update()
	return half_state
