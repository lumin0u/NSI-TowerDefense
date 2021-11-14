import pygame

import main
from interface import pictures
from position import Position

cursor_hand_reasons = {}

# constante: la largeur (et hauteur) en pixels que prend une tuile sur l'écran par niveau de zoom
# un niveau de zoom de 1.5 indique qu'une tuile prendra 60 pixels en largeur et en hauteur
PIXEL_PER_ZOOM = 40

# ~constantes: déclaration des variables des polices
FPS_FONT: pygame.font.Font = None
WAVE_FONT: pygame.font.Font = None
NEXT_WAVE_FONT: pygame.font.Font = None
TOWER_LVL_FONT: pygame.font.Font = None
PRICES_FONT: pygame.font.Font = None
LEVEL_BUTTON_FONT: pygame.font.Font = None
PAUSE_BUTTONS_FONT: pygame.font.Font = None
RESET_FONT: pygame.font.Font = None
INFO_FONT: pygame.font.Font = None


def load_fonts():
    """
        Chargement et initialisation des polices de pygame
        Cette fonction doit être appelée après l'initialisation du module pygame
    """
    global FPS_FONT, WAVE_FONT, NEXT_WAVE_FONT, TOWER_LVL_FONT, PRICES_FONT, LEVEL_BUTTON_FONT, PAUSE_BUTTONS_FONT, \
        RESET_FONT, INFO_FONT

    FPS_FONT = pygame.font.Font(None, 30)
    WAVE_FONT = pygame.font.Font(None, 40)
    NEXT_WAVE_FONT = pygame.font.Font(None, 30)
    TOWER_LVL_FONT = pygame.font.Font(None, 20)
    PRICES_FONT = pygame.font.Font(None, 23)
    LEVEL_BUTTON_FONT = pygame.font.Font(None, 50)
    PAUSE_BUTTONS_FONT = pygame.font.Font(None, 40)
    RESET_FONT = pygame.font.Font(None, 25)
    INFO_FONT = pygame.font.Font(None, 25)


def get_pixel_pos(game_pos, interface):
    """
        Retourne la position sur l'écran exprimée par des distances en pixels d'une position du jeu exprimée par des
        distances en tuiles
        Fonction réciproque de get_game_pos()
    :param game_pos: Position - la position exprimée en tuiles
    :param interface: Interface - l'instance de l'interface
    :return: Position - la position sur l'écran de la position passée en argument
    """
    return (game_pos - interface.half_camera_pos) * PIXEL_PER_ZOOM * interface.half_zoom + Position(main.SCREEN_WIDTH / 2, main.SCREEN_HEIGHT / 2)


def get_game_pos(pixel_pos, interface) -> Position:
    """
        Retourne la position du jeu d'une position sur l'écran
        Fonction réciproque de get_pixel_pos()
    :param pixel_pos: Position - la position exprimée en pixels
    :param interface: Interface - l'instance de l'interface
    :return: Position - la position en jeu de la position sur l'écran passée en argument
    """
    return (pixel_pos - Position(main.SCREEN_WIDTH / 2, main.SCREEN_HEIGHT / 2)) / PIXEL_PER_ZOOM / interface.half_zoom + interface.half_camera_pos


def draw_image(surface, position, image, new_size=None):
    """
        Dessine une image à la position donnée sur une surface, uniquement si l'image est dans le cadre
        La taille finale de l'image peut être redéfinie. Si elle n'est pas renseignée, l'image garde sa taille
    :param surface: Surface - la surface sur laquelle l'image doit être dessinée
    :param position: tuple - les coordonnées du coin haut gauche de l'image
    :param image: MyImage - l'image qui doit être dessinée
    :param new_size: tuple - optionnel, (width, height) indique la taille finale en pixels que devra prendre l'image
    """
    if image.get_rect().w == 0 and image.get_rect().h == 0:
        return
    
    built_image = image.build_image()
    
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


# fonction utilisée principalement pour les boutons
def highlight(base_image, highlight_alpha, border_width, border_alpha):
    """
        Retourne une version surlignée de l'image passée en paramètre
        Un masque blanc et une bordure plus ou moins transparents sont ajoutés à l'image
        L'image n'est pas modifiée en place
    :param base_image: Surface - l'image à surligner
    :param highlight_alpha: nombre - l'alpha du masque blanc ajouté à l'image
    :param border_width: nombre - la taille de la bordure en pixels
    :param border_alpha: nombre - l'alpha de la bordure
    :return: Surface - l'image construite
    """
    rect = base_image.get_rect()
    
    image = pictures.MyImage.void(rect.w, rect.h).build_image()
    
    # ajout du masque blanc à l'intéreur de la bordure, pour ne pas dessiner 2 couches
    inside = rect.inflate(min(0, -border_width), min(0, -border_width))
    pygame.draw.rect(image, (255, 255, 255, int(highlight_alpha * 255)), inside)
    
    # ajout des bordures
    pygame.draw.rect(image, (255, 255, 255, int(border_alpha * 255)), (0, 0, border_width, rect.h))
    pygame.draw.rect(image, (255, 255, 255, int(border_alpha * 255)), (0, 0, rect.w, border_width))
    pygame.draw.rect(image, (255, 255, 255, int(border_alpha * 255)), (rect.w - border_width, border_width, border_width, rect.h - border_width))
    pygame.draw.rect(image, (255, 255, 255, int(border_alpha * 255)), (border_width, rect.h - border_width, rect.w - border_width, border_width))
    
    # dessin du masque+bordure sur une copie de l'image
    image1 = base_image.copy()
    image1.blit(image, (0, 0))
    return image1


def smooth_stop(x, p=5):
    """
    :param x: float - un nombre entre 0 et 1 compris
    :param p: nombre - la puissance à laquelle est élevée 1-x
    :return: 1 - (1 - x)^p
    """
    s = 1 - x
    return 1 - s ** p


# https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame
def blitRotateCenter(surf, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)

    surf.blit(rotated_image, new_rect)


# chargement des images des particules
PARTICLES = {
    "smoke": pygame.transform.scale(pygame.image.load("resources/images/particles/smoke.png"), (32, 32)),
    "explosion": pygame.transform.scale(pygame.image.load("resources/images/particles/explosion.png"), (32, 32)),
    "freeze": pygame.transform.scale(pygame.image.load("resources/images/particles/freeze.png"), (32, 32)),
    
    "simple_break": pygame.transform.scale(pygame.image.load("resources/images/particles/simple_break.png"), (32, 32)),
    "robuste_break": pygame.transform.scale(pygame.image.load("resources/images/particles/robuste_break.png"), (32, 32)),
    "boss_break": pygame.transform.scale(pygame.image.load("resources/images/particles/boss_break.png"), (32, 32)),
    "rapide_break": pygame.transform.scale(pygame.image.load("resources/images/particles/rapide_break.png"), (32, 32))
}


def draw_particle(interface, smoke, elapsed_time):
    """
        Dessine une particule sur l'écran principal
        Le dessin des particules est séparé du dessin général pour optimiser la vitesse du dessin
    :param interface: Interface - l'instance de l'interface
    :param smoke: list - représentation d'une particule
    :param elapsed_time: nombre - temps écoulé depuis la dernière frame
    """
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
