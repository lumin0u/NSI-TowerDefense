from traceback import print_stack

import pygame
import sys
import game
import graphics
import levels
import listener
import board
import pictures
from position import *
import time

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

TICK_REAL_TIME = 0.1


def tick():
    for mob in the_game.mobs:
        mob.tick()
    for tower in (tile.tower for tile in the_game.board.tiles if type(tile) is board.BuildingTile and not tile.is_empty()):
        tower.tick()


def set_hand_reason(reason, value):
    graphics.cursor_hand_reasons[reason] = value


if __name__ == '__main__':
    pygame.init()
    
    pictures.load_pictures()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.RESIZABLE, vsync=True)
    
    the_game = game.Game(levels.all_levels[0])
    
    graphics_settings = graphics.GraphicsSettings()
    
    is_clicking = False
    
    last_frame = time.time()
    half_state = graphics.DEFAULT_HALF_STATE.copy()
    
    while True:
        this_frame = time.time()
        graphics.draw_frame(half_state, graphics_settings, screen, the_game, this_frame, last_frame)
        
        #print(cursor_hand_reasons)
        if any((v for v in graphics.cursor_hand_reasons.values())):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        for event in pygame.event.get():
            listener.catch_event(event, graphics_settings)
        
        time.sleep(max(0.0, 0.01 - this_frame + last_frame))
        last_frame = this_frame