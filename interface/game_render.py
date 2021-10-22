import math

import pygame

import main
from position import Direction
import interface.graphics as graphics


def _render_image_game(screen, interface, image, game_position, centered, image_scale=1.):
    half_state = interface.half_state
    
    corner_draw = graphics.get_pixel_pos(game_position, half_state.camera_pos, half_state.zoom)
    img_new_size = (math.ceil(graphics.PIXEL_PER_ZOOM * half_state.zoom * image_scale),) * 2
    n_scale = image.final_size
    img_new_size = (img_new_size[0] * n_scale[0], img_new_size[1] * n_scale[1])
    
    if centered:
        corner_draw -= Direction(img_new_size[0] / 2, img_new_size[1] / 2)

    corner_draw = corner_draw.to_tuple()
    
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
    
    elapsed_time = max(0.01, (time - last_frame))
    
    half_state.zoom = _pos_lerp(graphics_settings.zoom, half_state.zoom, elapsed_time)
    
    half_state.camera_pos = _pos_lerp(graphics_settings.camera_pos, half_state.camera_pos, elapsed_time)
    
    for tile in game_.level.tiles:
        _render_image_game(screen, interface, tile.get_render(time), tile.position, False)
        
    for mob in game_.mobs:
        if mob.id_ not in half_state.mobs_position:
            half_state.mobs_position[mob.id_] = mob.position
        
        half_state.mobs_position[mob.id_] = _pos_lerp(mob.position, half_state.mobs_position[mob.id_], elapsed_time)
        
        mob_img = mob.get_render(time).shaded(min(1, (mob.ticks_lived / 20) ** 3 + elapsed_time * 10))
        
        _render_image_game(screen, interface, mob_img, half_state.mobs_position[mob.id_], True)
