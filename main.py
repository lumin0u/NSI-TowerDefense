import pygame
import sys

pygame.init()
screen_width = 320
screen_height = 222

screen = pygame.display.set_mode((screen_width, screen_height))

if __name__ == '__main__':
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
