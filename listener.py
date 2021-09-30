import pygame
import sys
import main
from position import Position, TilePosition, Direction
import graphics

mouse_position = Position(0, 0)


def catch_event(event, interface):
    global mouse_position
    graphics_settings = interface.graphics_settings
    
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    
    elif event.type == pygame.MOUSEMOTION:
        # déplacement libre
        if pygame.mouse.get_pressed(3)[0]:
            main.set_hand_reason("free_camera", True)
            graphics_settings.camera_pos -= Position.of(event.rel) / 40 / graphics_settings.zoom
        else:
            main.set_hand_reason("free_camera", False)
        
        mouse_position = Position.of(pygame.mouse.get_pos())
    
    elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            for button in interface.buttons:
                if button.rect.move(button.position).collidepoint(pygame.mouse.get_pos()):
                    button.onclick()
        elif event.button == 4:
            last_zoom = graphics_settings.zoom
            graphics_settings.zoom *= 10 / 9
            
            # vive les maths
            mx = (1 - 1 / graphics_settings.zoom * last_zoom) * mouse_position.x + (
                        1 / graphics_settings.zoom * last_zoom) * main.SCREEN_WIDTH / 2
            my = (1 - 1 / graphics_settings.zoom * last_zoom) * mouse_position.y + (
                        1 / graphics_settings.zoom * last_zoom) * main.SCREEN_HEIGHT / 2
            
            shift = graphics_settings.camera_pos
            
            # on déplace la caméra pour donner l'impression d'un zoom vers le curseur
            graphics_settings.camera_pos = graphics.get_game_pos(Position(mx, my), shift, last_zoom)
        elif event.button == 5:
            last_zoom = graphics_settings.zoom
            graphics_settings.zoom *= 0.9
            
            # vive les maths
            mx = (1 - last_zoom / graphics_settings.zoom) * mouse_position.x + (
                        last_zoom / graphics_settings.zoom) * main.SCREEN_WIDTH / 2
            my = (1 - last_zoom / graphics_settings.zoom) * mouse_position.y + (
                        last_zoom / graphics_settings.zoom) * main.SCREEN_HEIGHT / 2
            
            shift = graphics_settings.camera_pos
            
            # on déplace la caméra pour donner l'impression d'un zoom vers le curseur
            graphics_settings.camera_pos = graphics.get_game_pos(Position(mx, my), shift, last_zoom)
    
    elif event.type == pygame.VIDEORESIZE:
        main.SCREEN_WIDTH = event.w
        main.SCREEN_HEIGHT = event.h
