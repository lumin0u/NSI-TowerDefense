import sys

import pygame

from interface import graphics, ui
import main
from position import Position

mouse_position = Position(0, 0)


def zoom(interface: ui.Interface, factor):
    last_zoom = interface.zoom
    nzoom = last_zoom * factor
    
    # vive les maths
    mx = (1 - last_zoom / nzoom) * mouse_position.x + (last_zoom / nzoom) * main.SCREEN_WIDTH / 2
    my = (1 - last_zoom / nzoom) * mouse_position.y + (last_zoom / nzoom) * main.SCREEN_HEIGHT / 2
    
    interface.zoom = nzoom
    shift = interface.camera_pos
    
    # on déplace la caméra pour donner l'impression d'un zoom vers le curseur
    interface.camera_pos = graphics.get_game_pos(Position(mx, my), interface)


def catch_event(event, interface):
    global mouse_position
    
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    
    elif event.type == pygame.MOUSEMOTION:
        # déplacement libre
        """if interface.can_free_move():
            if pygame.mouse.get_pressed(3)[0]:
                main.set_hand_reason("free_camera", True)
                interface.camera_pos -= Position.of(event.rel) / 40 / interface.zoom
            else:
                main.set_hand_reason("free_camera", False)"""
        
        mouse_position = Position.of(pygame.mouse.get_pos())
    
    elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            interface.mouse_down(1, pygame.mouse.get_pos())
        elif event.button == 4:
            if interface.zoom < 3:
                zoom(interface, 10 / 9)
        elif event.button == 5:
            if interface.zoom > 0.7:
                zoom(interface, 9 / 10)
    
    elif event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
            interface.mouse_up(1, pygame.mouse.get_pos())
    
    elif event.type == pygame.VIDEORESIZE:
        main.SCREEN_WIDTH = event.w
        main.SCREEN_HEIGHT = event.h
