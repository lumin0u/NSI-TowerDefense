import pygame
import math

import main
import interface.ui as ui
from position import Position, Direction
import interface.graphics as graphics


def _render_image_game(screen, interface, image, game_position, centered, image_scale=1.):
    graphics_settings = interface.graphics_settings
    half_state = interface.half_state
    
    if type(image) is tuple:
        image_scale = image[1] * image_scale
        image = image[0]
    
    corner_draw = graphics.get_pixel_pos(game_position, half_state.camera_pos, half_state.zoom)
    img_new_size = (math.ceil(graphics.PIXEL_PER_ZOOM * half_state.zoom * image_scale),) * 2
    
    if centered:
        corner_draw -= Direction(img_new_size[0] / 2, img_new_size[1] / 2)

    corner_draw = corner_draw.to_tuple()
    
    rect = corner_draw + img_new_size
    
    graphics.draw_image(screen, corner_draw, image, img_new_size)
    
    rect = pygame.rect.Rect(*(corner_draw + img_new_size))
    return rect


def _pos_lerp(a, b, elapsed_time):
    x = max(0.0, min(1.0, 7 * elapsed_time + 0.01))
    return a * x + b * (1 - x)


def _render_game(interface, screen, game_, time, last_frame):
    graphics_settings = interface.graphics_settings
    half_state = interface.half_state
    
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, main.SCREEN_WIDTH, main.SCREEN_HEIGHT))
    
    elapsed_time = max(0.01, time - last_frame)
    
    half_state.zoom = _pos_lerp(graphics_settings.zoom, half_state.zoom, elapsed_time)
    
    half_state.camera_pos = _pos_lerp(graphics_settings.camera_pos, half_state.camera_pos, elapsed_time)
    
    for tile in game_.level.tiles:
        img_new_size = _render_image_game(screen, interface, tile.get_render(time), tile.position, False)
        
        """if tile.is_clickable():
            img = pygame.surface.Surface((img_new_size.w, img_new_size.h)).convert_alpha()
            img.fill((255, 255, 255, 0))
            button = Button(interface, tile.onclick, (img_new_size.x, img_new_size.y), img, graphics.highlight(img, 0.15, 2, 0.8), "building_" + str(hash(tile.position)))
            add_button(screen, interface, button)"""
        
    for mob in game_.mobs:
        if mob.id_ not in half_state.mobs_position:
            half_state.mobs_position[mob.id_] = mob.position
        
        half_state.mobs_position[mob.id_] = _pos_lerp(mob.position, half_state.mobs_position[mob.id_], elapsed_time)
        
        _render_image_game(screen, interface, mob.get_render(time), half_state.mobs_position[mob.id_], True)
