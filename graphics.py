import pygame

import main
from position import Position

cursor_hand_reasons = {}

EMPTY_IMAGE = pygame.Surface((0, 0))


class GraphicsSettings:
    def __init__(self):
        self._zoom = 1
        self.camera_pos = Position(0, 0)
    
    @property
    def zoom(self):
        return self._zoom
    
    @zoom.setter
    def zoom(self, value):
        self._zoom = max(0.3, min(3, value))


PIXEL_PER_ZOOM = 40


def get_pixel_pos(game_pos, shift, zoom):
    return (game_pos - shift) * PIXEL_PER_ZOOM * zoom + Position(main.SCREEN_WIDTH / 2, main.SCREEN_HEIGHT / 2)


def get_game_pos(pixel_pos, shift, zoom):
    return (pixel_pos - Position(main.SCREEN_WIDTH / 2, main.SCREEN_HEIGHT / 2)) / PIXEL_PER_ZOOM / zoom + shift


def draw_image(surface: pygame.Surface, position: tuple, image: pygame.Surface,
               new_size: tuple = None):
    if image.get_rect().w == 0 and image.get_rect().h == 0:
        return
    
    # n'afficher que les images qui sont visibles dans la fenetre
    if new_size is not None:
        if surface.get_rect().colliderect(pygame.rect.Rect(*(position + new_size))):
            image = pygame.transform.smoothscale(image, new_size)
            surface.blit(image, position)
    else:
        if surface.get_rect().colliderect(image.get_rect().move(position)):
            surface.blit(image, position)


def highlight(base_image: pygame.Surface, highlight_alpha: float, border_width: float, border_alpha: float):
    image = base_image.copy()
    
    rect = image.get_rect()
    
    pygame.draw.rect(image, (255, 255, 255, 0), rect)
    
    pygame.draw.rect(image, (255, 255, 255, int(highlight_alpha * 255)), rect
                     .inflate(min(0, -border_width), min(0, -border_width)))
    
    pygame.draw.rect(image, (255, 255, 255, int(border_alpha * 255)), (0, 0, border_width, rect.h))
    pygame.draw.rect(image, (255, 255, 255, int(border_alpha * 255)), (0, 0, rect.w, border_width))
    pygame.draw.rect(image, (255, 255, 255, int(border_alpha * 255)), (rect.w - border_width, border_width, border_width, rect.h - border_width))
    pygame.draw.rect(image, (255, 255, 255, int(border_alpha * 255)), (border_width, rect.h - border_width, rect.w - border_width, border_width))
    
    image1 = base_image.copy()
    image1.blit(image, (0, 0))
    return image1
