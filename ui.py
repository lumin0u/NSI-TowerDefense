import math

import tiles
import game
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
        self.mobs_position = {}


class Interface:
    def __init__(self, game_):
        self._game = game_
        self.half_state = HalfState()
        self.graphics_settings = graphics.GraphicsSettings()
        self.volume = 2
    
    @property
    def game(self):
        return self._game


class Button:
    def __init__(self, onclick, position, img, hover_img, id_: str):
        self.onclick = onclick
        self._img = img
        self._hover_img = hover_img
        self._position = position
        self._id = id_
    
    @property
    def img(self):
        return self._img
    
    @property
    def hover_img(self):
        return self._hover_img
    
    @property
    def position(self):
        return self._position
    
    @property
    def id(self):
        return self._id
    

def render_button(screen, button):
    
    if pygame.rect.Rect(button.position + (button.img.get_width(), button.img.get_height())).collidepoint(
            pygame.mouse.get_pos()):
        graphics.draw_image(screen, button.position, button.hover_img)
        main.set_hand_reason("hover_button_" + str(hash(button.id)), True)
    else:
        graphics.draw_image(screen, button.position, button.img)
        main.set_hand_reason("hover_button_" + str(hash(button.id)), False)


def render(interface, game_, screen, time, last_frame):

    volume_img = pictures.PICTURES["volume_" + str(interface.volume)].get_img(time)
    volume_hover_img = volume_img.copy()
    volume_hover_img.blit(volume_img, (0, 0))
    
    volume = Button(lambda: (), (0, main.SCREEN_HEIGHT - volume_img.get_height()), volume_img, volume_hover_img, "volume")

    _render_game(interface.half_state, interface.graphics_settings, screen, game_, time, last_frame)
    render_button(screen, volume)
    
    pygame.display.update()


MOB_SIZE = 0.3

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
        graphics.draw_image(screen, corner_draw, img, img_new_size)
        
        if isinstance(tile, tiles.BuildingTile) and tile.is_empty():
            if pygame.rect.Rect(rect).collidepoint(pygame.mouse.get_pos()):
                main.set_hand_reason("hover_building_" + str(hash(tile.position)), True)
                graphics.draw_image(screen, corner_draw, pictures.PICTURES["mouse_hover"].get_img(time), img_new_size)
            else:
                main.set_hand_reason("hover_building_" + str(hash(tile.position)), False)
        
    for mob in game_.mobs:
        if mob.id_ not in half_state.mobs_position:
            half_state.mobs_position[mob.id_] = mob.position
        
        half_state.mobs_position[mob.id_] = half_state.mobs_position[mob.id_] * (1 - half_movement) + mob.position * half_movement
        
        corner_draw = graphics.get_pixel_pos(half_state.mobs_position[mob.id_] - Position(MOB_SIZE / 2, MOB_SIZE / 2), half_state.camera_pos, half_state.zoom).to_tuple()
        img_new_size = (math.ceil(RELATIVE_SIZE * MOB_SIZE), math.ceil(RELATIVE_SIZE * MOB_SIZE))
        rect = corner_draw + img_new_size
        
        img = mob.get_render(time)
        graphics.draw_image(screen, corner_draw, img, img_new_size)
