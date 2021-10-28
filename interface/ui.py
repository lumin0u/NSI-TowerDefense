import math

import pygame

import interface.pictures as pictures
import main
import tiles
from position import Position, Direction
import interface.graphics as graphics
from interface import game_render


TOOLBOX_WIDTH = 150

ZOOM_TRAVEL_TIME = 0.2


def lerp(a, b, m, nice_m=True):
    if nice_m:
        m = max(0, min(1, m))
    return b * m + a * (1 - m)


class Interface:
    def __init__(self, game_):
        self._game = game_
        self.volume = 2
        self.buttons = []
        self._click_start = "free"
        
        self.camera_pos = Position(0, 0)
        self.half_camera_pos = self.camera_pos
        
        self.zoom = 2
        self.half_zoom = 1 / 100
    
    @property
    def game(self):
        return self._game
    
    def mouse_down(self, mouse_button, mouse_pos):
        for button in self.buttons:
            if button.rect.move(button.position).collidepoint(pygame.mouse.get_pos()):
                self._click_start = "button" + str(hash(button.position))
                return
    
    def mouse_up(self, mouse_button, mouse_pos):
        for button in self.buttons:
            if "button" + str(hash(button.position)) == self._click_start and button.rect.move(button.position).collidepoint(pygame.mouse.get_pos()):
                button.onclick()
                return
        for tile in self.game.level.tiles:
            if tile.is_clickable() and tile.get_on_screen_rect(self).collidepoint(pygame.mouse.get_pos()):
                tile.onclick()
    
    def can_free_move(self):
        return self._click_start == "free"
    
    def is_clicking_button(self, button):
        return pygame.mouse.get_pressed(3)[0] and self._click_start == "button" + str(hash(button.position))


class Button:
    def __init__(self, interface, onclick, position, img, hover_img, id_: str):
        self._interface = interface
        self.onclick = onclick
        self._img = img
        self._hover_img = hover_img
        self._position = position
        self._id = id_
    
    @property
    def img(self):
        return self._img

    @property
    def hover_img(self):
        if self._interface.is_clicking_button(self):
            return self._hover_img.highlighted(0.3, 0, 0)
        return self._hover_img
    
    @property
    def rect(self):
        return self.img.get_rect()
    
    @property
    def position(self):
        return self._position
    
    @property
    def id(self):
        return self._id


def render(interface, game_, screen, current_tick, time, last_frame, relative_time):
    interface.buttons = []

    delta = time - last_frame
    
    if pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_z]:
        interface.camera_pos += Direction(0, -8 * delta / math.sqrt(interface.zoom))
    if pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_s]:
        interface.camera_pos += Direction(0, 8 * delta / math.sqrt(interface.zoom))
    if pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_q]:
        interface.camera_pos += Direction(-8 * delta / math.sqrt(interface.zoom), 0)
    if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]:
        interface.camera_pos += Direction(8 * delta / math.sqrt(interface.zoom), 0)
    
    interface.half_zoom = lerp(interface.half_zoom, interface.zoom, delta + 0.1)
    interface.half_camera_pos = lerp(interface.half_camera_pos, interface.camera_pos, delta + 0.1)
    
    game_render.render_game(interface, screen, current_tick, game_, time, last_frame, relative_time)
    
    show_ui(interface, game_, screen, current_tick, time, last_frame, relative_time)
    
    pygame.display.update()
    

def add_button(screen, interface, button):
    if pygame.rect.Rect(button.rect.move(button.position)).collidepoint(
            pygame.mouse.get_pos()):
        graphics.draw_image(screen, button.position, button.hover_img)
        main.set_hand_reason("hover_button_" + str(hash(button.id)), True)
    else:
        graphics.draw_image(screen, button.position, button.img)
        main.set_hand_reason("hover_button_" + str(hash(button.id)), False)
    
    interface.buttons.append(button)


def show_ui(interface, game_, screen, current_tick, time, last_frame, relative_time):
    volume_img = pictures.PICTURES["volume_" + str(interface.volume)].get_img()
    volume_hover_img = volume_img.copy().highlighted(0.15, 0, 0)
    
    def volume_onclick():
        interface.volume = (interface.volume - 1) % 3
        pygame.mixer.music.set_volume((interface.volume / 4) ** 2)
    
    volume = Button(interface, volume_onclick, (0, main.SCREEN_HEIGHT - volume_img.get_height()), volume_img, volume_hover_img, "volume")

    add_button(screen, interface, volume)
    
    """image = pygame.Surface((TOOLBOX_WIDTH + 10, main.SCREEN_HEIGHT + 10)).convert_alpha()
    image.fill((0, 0, 0, 0))
    image = graphics.highlight(image, 0.15, 2, 0.4)
    
    screen.blit(image, (main.SCREEN_WIDTH - TOOLBOX_WIDTH, -5))"""
    
    screen.blit(graphics.FPS_FONT.render(str(int(1 / (time - last_frame))), True, (150, 0, 200)), (0, 0))
