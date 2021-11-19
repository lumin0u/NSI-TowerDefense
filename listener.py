import sys

import pygame

import game
import userdata
from interface import graphics
import main
from position import Position


def zoom(interface, factor):
    """
        Augmente ou diminue le zoom du jeu et déplace la caméra vers la souris
    :param interface: Interface - l'instance de l'interface
    :param factor: nombre - facteur d'augmentation du zoom
    """
    last_zoom = interface.zoom
    
    # le nouveau zoom
    nzoom = last_zoom * factor
    
    # vive les maths
    mx = (1 - last_zoom / nzoom) * pygame.mouse.get_pos()[0] + (last_zoom / nzoom) * main.SCREEN_WIDTH / 2
    my = (1 - last_zoom / nzoom) * pygame.mouse.get_pos()[1] + (last_zoom / nzoom) * main.SCREEN_HEIGHT / 2
    
    interface.zoom = nzoom
    
    # on déplace la caméra pour donner l'impression d'un zoom vers le curseur
    interface.camera_pos = graphics.get_game_pos(Position(mx, my), interface)


def catch_event(event, interface):
    """
        Récupère et gère l'événement event
    :param event: l'événement de pygame
    :param interface: Interface - l'instance de l'interface
    """
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    
    elif event.type == pygame.MOUSEBUTTONDOWN:
        # clic gauche
        if event.button == 1:
            interface.mouse_down(1, pygame.mouse.get_pos())
        # molette vers l'avant
        elif event.button == 4:
            if interface.zoom < 3:
                zoom(interface, 10 / 9)
        # molette vers l'arrière
        elif event.button == 5:
            if interface.zoom > 0.7:
                zoom(interface, 9 / 10)
    
    elif event.type == pygame.MOUSEBUTTONUP:
        # clic gauche
        if event.button == 1:
            interface.mouse_up(game.GAME_INSTANCE, 1, pygame.mouse.get_pos())
    
    # redimensionnement de l'écran
    elif event.type == pygame.VIDEORESIZE:
        main.SCREEN_WIDTH = event.w
        main.SCREEN_HEIGHT = event.h
    
    elif event.type == pygame.KEYDOWN:
        # touche échap, permet de cacher une notification à l'écran (simule un appui sur le bouton OK) s'il y en a une
        # ou de mettre en pause et de l'enlever facilement sinon
        if event.key == pygame.K_ESCAPE:
            if interface.popup_text:
                if interface.popup_button_action:
                    interface.popup_button_action()
                interface.popup_text = None
                interface.popup_button_action = None
            elif game.GAME_INSTANCE:
                game.GAME_INSTANCE.paused = not game.GAME_INSTANCE.paused
        
        # k: touche de débug qui permet de débloquer tout les niveaux
        elif event.key == pygame.K_k:
            userdata.UNLOCKED_LEVELS = list(range(10))
