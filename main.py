import time

import pygame

import levels
import game
import listener
from interface import pictures, ui, graphics

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

TICK_REAL_TIME = 0.05

global current_tick
current_tick = 0


def tick():
    the_game.tick(get_current_tick())


def get_current_tick():
    return current_tick


def set_hand_reason(reason, value):
    graphics.cursor_hand_reasons[reason] = value


if __name__ == '__main__':
    pygame.init()
    
    pictures.load_pictures()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.RESIZABLE, vsync=True)
    
    levels.build_levels()
    the_game = game.Game(levels.ALL_LEVELS[0], 200)
    
    interface = ui.Interface(the_game)
    
    last_frame = time.time()
    last_tick = time.time()

    pygame.mixer.init()
    pygame.mixer.music.load("musics/HOME - Resting State - 14.mp3")
    pygame.mixer.music.play(1000)
    pygame.mixer.music.set_volume((interface.volume / 4) ** 2)
    
    while True:
        if time.time() > TICK_REAL_TIME + last_tick:
            tick()
            current_tick += 1
            last_tick = time.time()
        
        this_frame = time.time()
        ui.render(interface, the_game, screen, this_frame, last_frame, min(1., (this_frame - last_tick) / TICK_REAL_TIME))
        
        if any((v for v in graphics.cursor_hand_reasons.values())):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        for event in pygame.event.get():
            listener.catch_event(event, interface)
        
        time.sleep(max(0.0, 0.01 - this_frame + last_frame))
        last_frame = this_frame
