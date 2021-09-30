from traceback import print_stack
import pygame
import time
import sys

import levels
import game
import position
import tiles
import graphics
import listener
import pictures
import ui

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

TICK_REAL_TIME = 0.1


def tick(current_tick):
    the_game.tick(current_tick)


def set_hand_reason(reason, value):
    graphics.cursor_hand_reasons[reason] = value


if __name__ == '__main__':
    pygame.init()
    
    pictures.load_pictures()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.RESIZABLE, vsync=True)
    
    the_game = game.Game(levels.ALL_LEVELS[0], 200)
    
    interface = ui.Interface(the_game)
    
    is_clicking = False
    
    last_frame = time.time()
    last_tick = time.time()

    current_tick = 0
    
    while True:
        
        if time.time() > TICK_REAL_TIME + last_tick:
            tick(current_tick)
            current_tick += 1
            last_tick = time.time()
        
        this_frame = time.time()
        ui.render(interface, the_game, screen, this_frame, last_frame)
        
        if any((v for v in graphics.cursor_hand_reasons.values())):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        for event in pygame.event.get():
            listener.catch_event(event, interface)
        
        time.sleep(max(0.0, 0.01 - this_frame + last_frame))
        last_frame = this_frame
