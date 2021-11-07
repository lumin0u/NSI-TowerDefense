import math

import game
import pygame

import interface.pictures as pictures
import levels
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
    def __init__(self, screen):
        self._screen: pygame.Surface = screen
        self.volume = 2
        self.buttons = []
        self._click_start = "free"
        self.popup_tile: tiles.Tile = None
        self.popup_rect: pygame.Rect = None
        
        self.camera_pos = Position(0, 0)
        self.half_camera_pos = self.camera_pos
        
        self.zoom = 2
        self.half_zoom = 1 / 100
    
    @property
    def screen(self):
        return self._screen
    
    def mouse_down(self, mouse_button, mouse_pos):
        for button in self.buttons:
            if button.rect.move(button.position).collidepoint(pygame.mouse.get_pos()):
                self._click_start = button.id
                return
    
    def mouse_up(self, game_, mouse_button, mouse_pos):
        if not self.popup_tile or not self.popup_rect or not self.popup_rect.collidepoint(pygame.mouse.get_pos()):
            self.popup_tile = None
            self.popup_rect = None
            for button in self.buttons:
                if button.id == self._click_start and button.rect.move(button.position).collidepoint(pygame.mouse.get_pos()):
                    button.onclick()
                    return
            
            if game_:
                for tile in game_.level.tiles:
                    if tile.is_clickable() and tile.get_on_screen_rect(self).collidepoint(pygame.mouse.get_pos()):
                        self.popup_tile = tile
        else:
            for button in self.buttons:
                if button.id == self._click_start \
                        and button.rect.move(button.position).collidepoint(pygame.mouse.get_pos()) \
                        and button.id.startswith("buy"):
                    button.onclick()
                    return
    
    def can_free_move(self):
        return self._click_start == "free"
    
    def is_clicking_button(self, button):
        return pygame.mouse.get_pressed(3)[0] and self._click_start == button.id


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


def render(interface: Interface, game_: game.Game, time, last_frame, relative_time):
    pygame.draw.rect(interface.screen, (0, 0, 0), (0, 0, main.SCREEN_WIDTH, main.SCREEN_HEIGHT))
    
    interface.buttons = []
    main.clear_hand_reasons()

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
    
    if game_:
        game_render.render_game(interface, game_, time, last_frame, relative_time)
        
        if game_.paused:
            interface.screen.fill((100, 100, 100), special_flags=pygame.BLEND_MULT)
    
    show_ui(interface, game_, time, last_frame, relative_time)
    
    pygame.display.update()
    

def add_button(interface, button):
    if pygame.rect.Rect(button.rect.move(button.position)).collidepoint(
            pygame.mouse.get_pos()):
        graphics.draw_image(interface.screen, button.position, button.hover_img)
        main.set_hand_reason("hover_button_" + str(hash(button.id)), True)
    else:
        graphics.draw_image(interface.screen, button.position, button.img)
        main.set_hand_reason("hover_button_" + str(hash(button.id)), False)
    
    interface.buttons.append(button)



def show_ui(interface, game_: game.Game, time, last_frame, relative_time):
    if not game_ or game_.paused:
        volume_img = pictures.get("volume_" + str(interface.volume))
        volume_hover_img = volume_img.copy().highlighted(0.15, 0, 0)
        
        def volume_onclick():
            interface.volume = (interface.volume - 1) % 3
            pygame.mixer.music.set_volume((interface.volume / 4) ** 2)
        
        button = Button(interface, volume_onclick, (10, main.SCREEN_HEIGHT - volume_img.get_height() - 10), volume_img, volume_hover_img, "volume")
    
        add_button(interface, button)
    
    if game_:
        pause_img = pictures.get("pause")
        pause_hover_img = pause_img.copy().highlighted(0.15, 0, 0)
        
        def pause_onclick():
            game_.paused = not game_.paused
        
        button_pause = Button(interface, pause_onclick, (10, 10), pause_img, pause_hover_img, "pause")
        add_button(interface, button_pause)
        
        if game_.paused:
            pause_menu = pictures.MyImage.void(4 * 64, 4 * (2 * 8 + 2 * 32))
            pause_menu.blit(pictures.get("top").scaled_to((4 * 64, 4 * 8)), (0, 0))
            pause_menu.blit(pictures.get("body").scaled_to((4 * 64, 4 * 32)), (0, 4 * 8))
            pause_menu.blit(pictures.get("body").scaled_to((4 * 64, 4 * 32)), (0, 4 * (8 + 32)))
            pause_menu.blit(pictures.get("top").scaled_to((4 * 64, 4 * 8)).rotated(180), (0, 4 * (8 + 2 * 32)))
            
            menu_draw_pos = ((main.SCREEN_WIDTH - 4 * 64) / 2, (main.SCREEN_HEIGHT - 4 * (2 * 8 + 2 * 32)) / 2)
            
            resume_text_img = graphics.PAUSE_BUTTONS_FONT.render("Reprendre", True, (255, 255, 255, 127))
            resume_img = pictures.MyImage.void(215, resume_text_img.get_height() + 12)
            resume_img.blit(resume_text_img, ((215 - resume_text_img.get_width()) / 2, 6))
            
            resume_img.highlighted(0.15, 2, 0.6)
            resume_hover_img = resume_img.copy().highlighted(0.15, 0, 0)
            
            def resume_onclick():
                game_.paused = False
            
            resume_pos = (menu_draw_pos[0] + 20, menu_draw_pos[1] + 4 * 8 + 40)
            button_resume = Button(interface, resume_onclick, resume_pos, resume_img, resume_hover_img, "resume")
            
            #
            
            leave_text_img = graphics.PAUSE_BUTTONS_FONT.render("Quitter", True, (255, 255, 255, 127))
            leave_img = pictures.MyImage.void(215, leave_text_img.get_height() + 12)
            leave_img.blit(leave_text_img, ((215 - leave_text_img.get_width()) / 2, 6))
            
            leave_img.highlighted(0.15, 2, 0.6)
            leave_hover_img = leave_img.copy().highlighted(0.15, 0, 0)
            
            def leave_onclick():
                game.GAME_INSTANCE = None
            
            leave_pos = (menu_draw_pos[0] + 20, menu_draw_pos[1] + 4 * 8 + 4 * 32 + 40)
            button_leave = Button(interface, leave_onclick, leave_pos, leave_img, leave_hover_img, "leave")
            
            interface.screen.blit(pause_menu.build_image(), menu_draw_pos)
            add_button(interface, button_resume)
            add_button(interface, button_leave)
    else:
        for lvl in range(10):
            lvl_img = pictures.MyImage.void(80, 68)
            lvl_text_img = graphics.LEVEL_BUTTON_FONT.render(str(lvl + 1), True, (255, 255, 255, 127))
            lvl_img.highlighted(0, 2, 0.6)
            txt_rel_pos = ((lvl_img.get_width() - lvl_text_img.get_width()) / 2, (lvl_img.get_height() - lvl_text_img.get_height()) / 2)
            lvl_img.blit(lvl_text_img, txt_rel_pos)
            lvl_hover_img = lvl_img.copy().highlighted(0.15, 0, 0)
            
            def lvl_onclick(lvl):
                def lvl_onclick_():
                    game.GAME_INSTANCE = game.Game(levels.ALL_LEVELS[lvl])
                return lvl_onclick_
            
            button_pos = (100 * (lvl % 5) + (main.SCREEN_WIDTH - 480) / 2, 100 * (lvl // 5) + (main.SCREEN_HEIGHT - 200) / 2)
            button = Button(interface, lvl_onclick(lvl), button_pos, lvl_img, lvl_hover_img, "lvl" + str(lvl))
        
            add_button(interface, button)
    
    if time != last_frame:
        interface.screen.blit(graphics.FPS_FONT.render(str(int(1 / (time - last_frame))), True, (150, 0, 200)), (0, 0))
