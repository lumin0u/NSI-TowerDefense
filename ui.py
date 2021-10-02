import math

import pygame

import pictures
import main
from position import Position, Direction
import graphics

pictures.load_picture("volume_0", "buttons/")
pictures.load_picture("volume_1", "buttons/")
pictures.load_picture("volume_2", "buttons/")


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
    
    volume_img = pictures.PICTURES["volume_" + str(interface.volume)].get_img(time)
    volume_hover_img = graphics.highlight(volume_img, 0.15, 0, 0)
    
    def volume_onclick():
        interface.volume = (interface.volume - 1) % 3
        pygame.mixer.music.set_volume((interface.volume / 4) ** 2)
    
    volume = Button(interface, volume_onclick, (0, main.SCREEN_HEIGHT - volume_img.get_height()), volume_img, volume_hover_img, "volume")

    _render_game(interface, screen, game_, time, last_frame)
    add_button(screen, interface, volume)
    
    font = pygame.font.Font(None, 30)
    screen.blit(font.render(str(int(1 / (time - last_frame))), True, (150, 0, 200)), (0, 0))
    
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


MOB_SIZE = 0.5


def _render_image_game(screen, interface, image, game_position, centered, image_scale=1.):
    graphics_settings = interface.graphics_settings
    half_state = interface.half_state
    
    corner_draw = graphics.get_pixel_pos(game_position, half_state.camera_pos, half_state.zoom)
    img_new_size = (math.ceil(graphics.PIXEL_PER_ZOOM * half_state.zoom * image_scale),) * 2
    
    if centered:
        corner_draw -= Direction(img_new_size[0] / 2, img_new_size[1] / 2)

    corner_draw = corner_draw.to_tuple()
    
    rect = corner_draw + img_new_size
    
    graphics.draw_image(screen, corner_draw, image, img_new_size)
    
    return pygame.rect.Rect(*(corner_draw + img_new_size))


def pos_lerp(a, b, elapsed_time):
    x = max(0.0, min(1.0, 7 * elapsed_time + 0.01))
    return a * x + b * (1 - x)


def _render_game(interface, screen, game_, time, last_frame):
    graphics_settings = interface.graphics_settings
    half_state = interface.half_state
    
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, main.SCREEN_WIDTH, main.SCREEN_HEIGHT))
    
    elapsed_time = max(0.01, time - last_frame)
    
    half_state.zoom = pos_lerp(graphics_settings.zoom, half_state.zoom, elapsed_time)
    
    half_state.camera_pos = pos_lerp(graphics_settings.camera_pos, half_state.camera_pos, elapsed_time)
    
    for tile in game_.level.tiles:
        img_new_size = _render_image_game(screen, interface, tile.get_render(time), tile.position, False)
        
        if tile.is_clickable():
            img = pygame.surface.Surface((img_new_size.w, img_new_size.h)).convert_alpha()
            img.fill((255, 255, 255, 0))
            button = Button(interface, tile.onclick, (img_new_size.x, img_new_size.y), img, graphics.highlight(img, 0.15, 2, 0.8), "building_" + str(hash(tile.position)))
            add_button(screen, interface, button)
            if img.get_rect().collidepoint(pygame.mouse.get_pos()):
                main.set_hand_reason("hover_building_" + str(hash(tile.position)), True)
            else:
                main.set_hand_reason("hover_building_" + str(hash(tile.position)), False)
        
    for mob in game_.mobs:
        if mob.id_ not in half_state.mobs_position:
            half_state.mobs_position[mob.id_] = mob.position
        
        half_state.mobs_position[mob.id_] = pos_lerp(mob.position, half_state.mobs_position[mob.id_], elapsed_time)
        
        _render_image_game(screen, interface, mob.get_render(time), half_state.mobs_position[mob.id_], True, MOB_SIZE)
