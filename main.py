import time

import pygame

import pricing

pygame.init()

import levels
import game
import listener
from interface import pictures, ui, graphics

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

TICK_REAL_TIME = 0.05


def _tick():
    if game.GAME_INSTANCE:
        game.GAME_INSTANCE.tick()


def set_hand_reason(reason, value):
    graphics.cursor_hand_reasons[reason] = value


def clear_hand_reasons():
    graphics.cursor_hand_reasons.clear()
    

def main():
    pictures.load_pictures()
    levels.build_levels()
    pricing.load()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.RESIZABLE)
    
    interface = ui.Interface(screen)
    interface.volume = 0
    
    last_frame = time.time()
    last_tick = time.time()
    
    MUSICS_FILES = [
        "musics/HOME - Resting State - 14.mp3",
        "musics/buck.mp3"
    ]

    pygame.mixer.init()
    pygame.mixer.music.load("musics/HOME - Resting State - 14.mp3")
    pygame.mixer.music.play(1000)
    pygame.mixer.music.set_volume((interface.volume / 4) ** 2)
    
    while True:
        if time.time() > TICK_REAL_TIME + last_tick:
            _tick()
            last_tick = time.time()
        
        this_frame = time.time()
        ui.render(interface, game.GAME_INSTANCE, this_frame, last_frame, min(1., (this_frame - last_tick) / TICK_REAL_TIME))
        
        if any((v for v in graphics.cursor_hand_reasons.values())):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        for event in pygame.event.get():
            listener.catch_event(event, interface)
        
        time.sleep(max(0.0, 0.01 - this_frame + last_frame))
        last_frame = this_frame


if __name__ == '__main__':
    main()
