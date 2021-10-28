import math

import pygame

import main
import tiles
from position import Direction, Position
from interface import graphics, ui, pictures
from mobs import mob


def _render_image_game(screen, interface, image, game_position, centered, relative_time):
    corner_draw = graphics.get_pixel_pos(game_position, interface)
    img_new_size = (math.ceil(graphics.PIXEL_PER_ZOOM * interface.half_zoom),) * 2
    n_scale = image.final_size
    img_new_size = (img_new_size[0] * n_scale[0], img_new_size[1] * n_scale[1])
    
    if centered:
        corner_draw -= Direction(img_new_size[0] / 2, img_new_size[1] / 2)

    corner_draw = corner_draw.to_tuple()
    
    graphics.draw_image(screen, corner_draw, image, img_new_size)
    
    rect = pygame.rect.Rect(*(corner_draw + img_new_size))
    return rect


def render_game(interface, screen, current_tick, game_, time, last_frame, relative_time):
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, main.SCREEN_WIDTH, main.SCREEN_HEIGHT))
    
    elapsed_time = max(0.001, (time - last_frame))
    
    for tile in game_.level.tiles:
        _render_image_game(screen, interface, tile.get_render(time), tile.position, False, relative_time)
        if isinstance(tile, tiles.CastleTile):
            bar_nb = max(0, tile.tower.health * 13 // tile.tower.max_health)
            bar_img = pictures.PICTURES["health" + str(int(bar_nb))].get_img()
            bar_img.final_scaled(0.8)
            bar_img.smoothscaling = False
            
            _render_image_game(screen, interface, bar_img, tile.position.middle() + Position(0, 0.6), True, relative_time)
        
    for entity in game_.entities:
        if entity.is_dead():
            continue
        
        pos = ui.lerp(entity.last_position, entity.position, relative_time)
        
        mob_img = entity.get_render(time)
        
        if isinstance(entity, mob.Mob):

            bar_nb = entity.health * 13 // entity.max_health
            bar_img = pictures.PICTURES["health" + str(int(bar_nb))].get_img()
            bar_img = bar_img.final_scaled(bar_img.get_width() / 128 * 1.5)
            bar_img.smoothscaling = False
            
            if (entity.ticks_lived + relative_time) * 0.05 < 1:
                mob_img.shaded(((entity.ticks_lived + relative_time) * 0.05) ** 3)
                bar_img.shaded(((entity.ticks_lived + relative_time) * 0.05) ** 3)
            
            _render_image_game(screen, interface, bar_img, pos + Position(0, mob_img.final_size[1] * 0.8), True, relative_time)
        
        _render_image_game(screen, interface, mob_img, pos, True, relative_time)
    
    text_img1 = graphics.WAVE_FONT.render("VAGUE " + str(game_.wave + 1), True, (170, 50, 50))
    screen.blit(text_img1, ((main.SCREEN_WIDTH - text_img1.get_width()) / 2, 10))

    if game_.btwn_waves:
        next_wave_text = "Vague suivante \u2022 " + str(int((game_.next_wave_date - current_tick) * main.TICK_REAL_TIME + 1))
        
        text_img2 = pictures.MyImage(graphics.NEXT_WAVE_FONT.render(next_wave_text, True, (150, 40, 40)))
        text_img2_hover = pictures.MyImage(graphics.NEXT_WAVE_FONT.render(next_wave_text, True, (200, 60, 60)))
        
        button_pos = ((main.SCREEN_WIDTH - text_img2.get_width()) / 2, 10 + text_img1.get_height())
        
        def next_wave_action():
            game_.next_wave_date = current_tick - 1
        
        next_wave_button = ui.Button(interface, next_wave_action, button_pos, text_img2, text_img2_hover, "next_wave")
        ui.add_button(screen, interface, next_wave_button)
    else:
        main.set_hand_reason("hover_button_" + str(hash("next_wave")), False)
