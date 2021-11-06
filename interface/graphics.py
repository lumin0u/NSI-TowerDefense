import pygame

import main
from position import Position

cursor_hand_reasons = {}

EMPTY_IMAGE = pygame.Surface((0, 0))

PIXEL_PER_ZOOM = 40

FPS_FONT: pygame.font.Font = pygame.font.Font(None, 30)
WAVE_FONT: pygame.font.Font = pygame.font.Font(None, 40)
NEXT_WAVE_FONT: pygame.font.Font = pygame.font.Font(None, 30)
TOWER_LVL_FONT: pygame.font.Font = pygame.font.Font(None, 20)
PRICES_FONT: pygame.font.Font = pygame.font.Font(None, 23)


def get_pixel_pos(game_pos, interface) -> Position:
    return (game_pos - interface.half_camera_pos) * PIXEL_PER_ZOOM * interface.half_zoom + Position(main.SCREEN_WIDTH / 2, main.SCREEN_HEIGHT / 2)


def get_game_pos(pixel_pos, interface) -> Position:
    return (pixel_pos - Position(main.SCREEN_WIDTH / 2, main.SCREEN_HEIGHT / 2)) / PIXEL_PER_ZOOM / interface.half_zoom + interface.half_camera_pos


def draw_image(surface: pygame.Surface, position: tuple, image, new_size: tuple = None):
    if image.get_rect().w == 0 and image.get_rect().h == 0:
        return
    
    built_image: pygame.Surface = image.build_image()
    
    # n'afficher que les images qui sont visibles dans la fenetre
    if new_size is not None:
        if surface.get_rect().colliderect(pygame.rect.Rect(*(position + new_size))):
            if image.smoothscaling:
                built_image = pygame.transform.smoothscale(built_image, (int(new_size[0]), int(new_size[1])))
            else:
                built_image = pygame.transform.scale(built_image, (int(new_size[0]), int(new_size[1])))
            surface.blit(built_image, position)
    else:
        if surface.get_rect().colliderect(image.get_rect().move(position)):
            surface.blit(built_image, position)


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
