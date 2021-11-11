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
LEVEL_BUTTON_FONT: pygame.font.Font = pygame.font.Font(None, 50)
PAUSE_BUTTONS_FONT: pygame.font.Font = pygame.font.Font(None, 40)
RESET_FONT: pygame.font.Font = pygame.font.Font(None, 25)
INFO_FONT: pygame.font.Font = pygame.font.Font(None, 25)


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


def smooth_stop(x, p=5):
    s = 1 - x
    return 1 - s ** p


def blitRotateCenter(surf, image, topleft, angle):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)

    surf.blit(rotated_image, new_rect)


PARTICLES = {
    "smoke": pygame.transform.scale(pygame.image.load("resources/images/smoke.png"), (32, 32)),
    "explosion": pygame.transform.scale(pygame.image.load("resources/images/explosion.png"), (32, 32)),
    
    "simple_break": pygame.transform.scale(pygame.image.load("resources/images/simple_break.png"), (32, 32)),
    "robuste_break": pygame.transform.scale(pygame.image.load("resources/images/robuste_break.png"), (32, 32)),
    "boss_break": pygame.transform.scale(pygame.image.load("resources/images/boss_break.png"), (32, 32)),
    "rapide_break": pygame.transform.scale(pygame.image.load("resources/images/rapide_break.png"), (32, 32))
}


def draw_particle(interface, smoke, elapsed_time):
    if smoke[5] > smoke[7]:
        return
    
    rel_life = smoke[5] / smoke[7]
    m = smooth_stop(rel_life, smoke[6])
    
    dir_ = get_pixel_pos(Position.of(smoke[1]), interface).to_tuple()
    
    rotation = smoke[2] + smoke[3] * m
    position = get_pixel_pos(Position.of(smoke[0]) + Position.of(smoke[1]) * m, interface).to_tuple()
    alpha = 255 - int(255 * rel_life)
    scale = (0.5 + rel_life * 2) * smoke[4] * interface.half_zoom / 2
    
    img = (PARTICLES[smoke[8]]).copy().convert_alpha()

    position = (position[0] - img.get_width() / 2 * scale, position[1] - img.get_height() / 2 * scale)
    
    img.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MULT)
    img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))

    blitRotateCenter(interface.screen, img, position, rotation)
    
    smoke[5] += elapsed_time
