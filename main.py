import pygame
import sys
import graphics
from game import Game
from board import Board
from position import Position, TilePosition, Direction
import time

pygame.init()
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

TICK_REAL_TIME = 0.1


if __name__ == '__main__':
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    the_game = Game(Board(TilePosition(0, 1), TilePosition(5, 2)))
    
    graphics_settings = graphics.GraphicsSettings()
    
    mouse_position = Position(0, 0)
    
    is_clicking = False
    
    last_frame = time.monotonic()
    while True:
        relative_time = time.monotonic() - last_frame
        last_frame = time.monotonic()
        graphics.draw_frame(graphics_settings, screen, the_game, relative_time)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEMOTION:
                mouse_position = Position.of(pygame.mouse.get_pos())
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    graphics_settings.zoom -= 0.1
                    graphics_settings.camera_pos += mouse_position
                elif event.button == 5:
                    graphics_settings.zoom += 0.1
