import pygame
import sys
import graphics
from game import Game
from board import Board
import board
from position import Position, TilePosition, Direction
import time

pygame.init()
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

TICK_REAL_TIME = 0.1


def tick():
    for mob in the_game.mobs:
        mob.tick()
    for tower in (tile.tower for tile in the_game.board.tiles if type(tile) is board.BuildingTile and not tile.is_empty()):
        tower.tick()


if __name__ == '__main__':
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    the_game = Game(Board(TilePosition(0, 0), TilePosition(2, 0)))
    
    graphics_settings = graphics.GraphicsSettings()
    
    mouse_position = Position(0, 0)
    
    is_clicking = False
    
    last_frame = time.time()
    
    while True:
        this_frame = time.time()
        graphics.draw_frame(graphics_settings, screen, the_game, this_frame, last_frame)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed(3)[0]:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    graphics_settings.camera_pos -= Position.of(event.rel) / 40 / graphics_settings.zoom
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                
                mouse_position = Position.of(pygame.mouse.get_pos())

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    last_zoom = graphics_settings.zoom
                    graphics_settings.zoom *= 10/9
                    
                    mx = (1 - 1/graphics_settings.zoom * last_zoom) * mouse_position.x + (1/graphics_settings.zoom * last_zoom) * SCREEN_WIDTH / 2
                    my = (1 - 1/graphics_settings.zoom * last_zoom) * mouse_position.y + (1/graphics_settings.zoom * last_zoom) * SCREEN_HEIGHT / 2

                    shift = graphics_settings.camera_pos
                    
                    graphics_settings.camera_pos = graphics.get_game_pos(Position(mx, my), shift, last_zoom)
                elif event.button == 5:
                    last_zoom = graphics_settings.zoom
                    graphics_settings.zoom *= 0.9
                    
                    mx = (1 - 1/graphics_settings.zoom * last_zoom) * mouse_position.x + (1/graphics_settings.zoom * last_zoom) * SCREEN_WIDTH / 2
                    my = (1 - 1/graphics_settings.zoom * last_zoom) * mouse_position.y + (1/graphics_settings.zoom * last_zoom) * SCREEN_HEIGHT / 2

                    shift = graphics_settings.camera_pos
                    
                    graphics_settings.camera_pos = graphics.get_game_pos(Position(mx, my), shift, last_zoom)
        
        time.sleep(max(0.0, 0.01 - this_frame + last_frame))
        last_frame = this_frame
