import math

import pygame

import interface.pictures as pictures
import main
from position import Position, Direction
import interface.graphics as graphics
from interface.game_render import _render_game

pictures.load_picture("volume_0", "buttons/")
pictures.load_picture("volume_1", "buttons/")
pictures.load_picture("volume_2", "buttons/")


TOOLBOX_WIDTH = 150


class HalfState:
    def __init__(self):
        self.camera_pos = Position(0, 0)
        self.zoom = 1 / 100
        self.mobs_position = {}


class Interface:
    def __init__(self, game_):
        self._game = game_
        self.half_state = HalfState()
        self.graphics_settings = graphics.GraphicsSettings()
        self.volume = 2
        self.buttons = []
        self._click_start = "free"
    
    @property
    def game(self):
        return self._game
    
    def mouse_down(self, mouse_button, mouse_pos):
        for button in self.buttons:
            if button.rect.move(button.position).collidepoint(pygame.mouse.get_pos()):
                button.onclick()
                self._click_start = "button" + str(hash(button.position))
                return
        if pygame.mouse.get_pos()[0] + TOOLBOX_WIDTH > main.SCREEN_WIDTH:
            self._click_start = "toolbox"
        else:
            self._click_start = "free"
    
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
            return graphics.highlight(self._hover_img, 0.3, 0, 0)
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


def render(interface, game_, screen, time, last_frame):
    interface.buttons = []
    
    _render_game(interface, screen, game_, time, last_frame)
    
    show_ui(interface, game_, screen, time, last_frame)
    
    pygame.display.update()
    

def add_button(screen, interface, button):
    clicking = pygame.mouse.get_pressed(3)[0]
    
    if pygame.rect.Rect(button.rect.move(button.position)).collidepoint(
            pygame.mouse.get_pos()):
        graphics.draw_image(screen, button.position, button.hover_img)
        main.set_hand_reason("hover_button_" + str(hash(button.id)), True)
    else:
        graphics.draw_image(screen, button.position, button.img)
        main.set_hand_reason("hover_button_" + str(hash(button.id)), False)
    
    interface.buttons.append(button)

def show_ui(interface, game_, screen, time, last_frame):
    volume_img = pictures.PICTURES["volume_" + str(interface.volume)].get_img(time)
    volume_hover_img = graphics.highlight(volume_img, 0.15, 0, 0)
    
    def volume_onclick():
        interface.volume = (interface.volume - 1) % 3
        pygame.mixer.music.set_volume((interface.volume / 4) ** 2)
    
    volume = Button(interface, volume_onclick, (0, main.SCREEN_HEIGHT - volume_img.get_height()), volume_img, volume_hover_img, "volume")

    add_button(screen, interface, volume)
    
    image = pygame.Surface((TOOLBOX_WIDTH + 10, main.SCREEN_HEIGHT + 10)).convert_alpha()
    image.fill((0, 0, 0, 0))
    image = graphics.highlight(image, 0.15, 2, 0.4)
    
    screen.blit(image, (main.SCREEN_WIDTH - TOOLBOX_WIDTH, -5))
    
    font = pygame.font.Font(None, 30)
    screen.blit(font.render(str(int(1 / (time - last_frame))), True, (150, 0, 200)), (0, 0))
