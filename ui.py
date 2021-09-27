import math

import tiles
from game import Game
import pygame
import pictures
import main
from position import Position, TilePosition, Direction
import graphics

pictures.load_picture("volume_0", "buttons/")
pictures.load_picture("volume_1", "buttons/")
pictures.load_picture("volume_2", "buttons/")


class HalfState:
    def __init__(self):
        self.camera_pos = Position(0, 0)
        self.zoom = 1 / 100


class Interface:
    def __init__(self, game):
        self._game = game
        self.half_state = HalfState()
        self.graphics_settings = graphics.GraphicsSettings()
        self.volume = 2
    
    @property
    def game(self):
        return self._game


def _render_button(screen, time, button_img, button_img_pos):
    screen.blit(button_img, button_img_pos)
    
    if pygame.rect.Rect(button_img_pos + (button_img.get_width(), button_img.get_height())).collidepoint(
            pygame.mouse.get_pos()):
        graphics.draw_image(screen, button_img_pos, button_img)
        main.set_hand_reason("hover_button_" + str(hash(button_img_pos)), True)
    else:
        main.set_hand_reason("hover_button_" + str(hash(button_img_pos)), False)


def render(interface, game, screen, time, last_frame):
    
    volume_img = pictures.PICTURES["volume_" + str(interface.volume)].get_img(time, None)
    volume_img_pos = (0, main.SCREEN_HEIGHT - volume_img.get_height())

    _render_game(interface.half_state, interface.graphics_settings, screen, game, time, last_frame)
    _render_button(screen, time, volume_img, volume_img_pos)
    
    pygame.display.update()


def _render_game(half_state, graphics_settings, screen, game_, time, last_frame):
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, main.SCREEN_WIDTH, main.SCREEN_HEIGHT))
    
    elapsed_time = max(0.01, time - last_frame)
    half_movement = min(1., 7 * elapsed_time)
    
    half_state.zoom = half_state.zoom * (1 - half_movement) + graphics_settings.zoom * half_movement
    
    half_state.camera_pos = half_state.camera_pos * (
                1 - half_movement) + graphics_settings.camera_pos * half_movement
    
    RELATIVE_SIZE = graphics.PIXEL_PER_ZOOM * half_state.zoom
    
    for tile in game_.board.tiles:
        # concatenation de (cornerX, cornerY) et de (width, height)
        corner_draw = graphics.get_pixel_pos(tile.position, half_state.camera_pos, half_state.zoom).to_tuple()
        img_new_size = (math.ceil(RELATIVE_SIZE), math.ceil(RELATIVE_SIZE))
        rect = corner_draw + img_new_size
        
        img = tile.get_render(time)
        graphics.draw_image(screen, corner_draw, pygame.transform.smoothscale(img, img_new_size))
        
        if isinstance(tile, tiles.BuildingTile) and tile.is_empty():
            if pygame.rect.Rect(rect).collidepoint(pygame.mouse.get_pos()):
                main.set_hand_reason("hover_building_" + str(hash(tile.position)), True)
                graphics.draw_image(screen, corner_draw, pygame.transform.smoothscale(pictures.PICTURES["mouse_hover"].get_img(time, None), img_new_size))
            else:
                main.set_hand_reason("hover_building_" + str(hash(tile.position)), False)