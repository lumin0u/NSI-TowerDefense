import math
import random
from typing import Union

import pygame

import game
import interface.pictures as pictures
import levels
import main
import strings
import tiles
import userdata
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
        global INTERFACE_INSTANCE
        INTERFACE_INSTANCE = self
        
        self._screen: pygame.Surface = screen
        self.volume = 2
        self.buttons = []
        self._click_start = "free"
        self.popup_tile: tiles.Tile = None
        self.popup_rect: pygame.Rect = None
        self.background_shade = 0
        self.smokes = []
        
        self.popup_text: list[str] = None
        self.popup_button_action = None
        
        self.camera_pos = Position(0, 0)
        self._half_camera_pos = self.camera_pos
        
        self.zoom = 2
        self._half_zoom = 1 / 100
       
    def _aroundrandom(self, scale):
        return random.random() * (random.random() * scale - scale / 2)
    
    def new_smoke(self, position, scale=1., dir_: Union[tuple, float, int] = 50, randomizer=0.5, speed=5, lifetime=2, img_name="smoke"):
        if dir_ and type(dir_) is tuple:
            rand_angle = random.random() * 2 * math.pi
            angle = math.atan2(dir_[1], dir_[0])
            dir_change = (1 + self._aroundrandom(randomizer))
            dir_ = math.sqrt(dir_[0] ** 2 + dir_[1] ** 2) * dir_change
            angle += math.atan(self._aroundrandom(randomizer)) / dir_change
            x = math.cos(angle) * dir_
            y = math.sin(angle) * dir_
            smoke = [position, (x, y), random.random() * 360, random.random() * 720 - 360, scale, 0, speed, lifetime, img_name]
        else:
            dir_ = float(dir_) * (1 + self._aroundrandom(randomizer))
            angle = random.random() * 2 * math.pi
            x = math.cos(angle) * dir_
            y = math.sin(angle) * dir_
            smoke = [position, (x, y), random.random() * 360, random.random() * 720 - 360, scale, 0, speed, lifetime, img_name]
            
        self.smokes.append(smoke)
        return smoke
    
    @property
    def screen(self):
        return self._screen
    
    @property
    def half_camera_pos(self):
        return self._half_camera_pos
    
    @property
    def half_zoom(self):
        return self._half_zoom
    
    def update_halves(self, delta):
        self._half_zoom = lerp(self.half_zoom, self.zoom, delta + 0.1)
        self._half_camera_pos = lerp(self.half_camera_pos, self.camera_pos, delta + 0.1)
    
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


INTERFACE_INSTANCE: Interface = None


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


def render(interface: Interface, game_, time, last_frame, relative_time):
    if game_ and game_.game_beaten:
        pygame.draw.rect(interface.screen, (0, 40 * interface.background_shade, 0), (0, 0, main.SCREEN_WIDTH, main.SCREEN_HEIGHT))
        if interface.background_shade < 1:
            interface.background_shade += 0.001
    else:
        pygame.draw.rect(interface.screen, (0, 0, 0), (0, 0, main.SCREEN_WIDTH, main.SCREEN_HEIGHT))
        interface.background_shade = 0
    
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
        
    interface.update_halves(delta)
    
    if game_:
        game_render.render_game(interface, game_, time, last_frame, relative_time)
        
        if game_.paused:
            interface.screen.fill((100, 100, 100), special_flags=pygame.BLEND_MULT)
    
    show_ui(interface, game_, time, last_frame, relative_time)

    for smoke in interface.smokes:
        if smoke[5] > smoke[7]:
            interface.smokes.remove(smoke)
            continue
        graphics.draw_particle(interface, smoke, time - last_frame)
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


def show_ui(interface, game_, time, last_frame, relative_time):
    if not game_ or game_.paused:
        volume_img = pictures.get("volume_" + str(interface.volume))
        volume_hover_img = volume_img.copy().highlighted(0.15, 0, 0)
        
        def volume_onclick():
            interface.volume = (interface.volume - 1) % 3
            pygame.mixer.music.set_volume((interface.volume / 4) ** 2)
        
        button = Button(interface, volume_onclick, (10, main.SCREEN_HEIGHT - volume_img.get_height() - 10), volume_img, volume_hover_img, "volume")
    
        add_button(interface, button)
    
    if interface.popup_text and len(interface.popup_text) > 0:
        popup_menu = pictures.MyImage.void(4 * 64, 4 * (2 * 8 + 2 * 32))
        popup_menu.blit(pictures.get("top").scaled_to((4 * 64, 4 * 8)), (0, 0))
        popup_menu.blit(pictures.get("body").scaled_to((4 * 64, 4 * 32)), (0, 4 * 8))
        popup_menu.blit(pictures.get("body").scaled_to((4 * 64, 4 * 32)), (0, 4 * (8 + 32)))
        popup_menu.blit(pictures.get("top").scaled_to((4 * 64, 4 * 8)).rotated(180), (0, 4 * (8 + 2 * 32)))
    
        menu_draw_pos = ((main.SCREEN_WIDTH - 4 * 64) / 2, (main.SCREEN_HEIGHT - 4 * (2 * 8 + 2 * 32)) / 2)
        
        line_offset = 20
        for line in interface.popup_text:
            if line and line != "":
                text_img = graphics.INFO_FONT.render(line, True, (255, 255, 255, 127))
                
                text_pos = ((popup_menu.get_width() - text_img.get_width()) // 2, int(line_offset))
                popup_menu.blit(text_img, text_pos)

            line_offset += graphics.INFO_FONT.get_height() * 1.5
    
        ok_text_img = graphics.PAUSE_BUTTONS_FONT.render("OK", True, (255, 255, 255, 127))
        ok_img = pictures.MyImage.void(70, ok_text_img.get_height() + 12)
        ok_img.blit(ok_text_img, ((70 - ok_text_img.get_width()) / 2, 6))
    
        ok_img.highlighted(0.15, 2, 0.6)
        ok_hover_img = ok_img.copy().highlighted(0.15, 0, 0)
    
        def ok_onclick():
            interface.popup_text = None
            action = interface.popup_button_action
            interface.popup_button_action = None
            if action:
                action()
    
        ok_pos = (menu_draw_pos[0] + 160, menu_draw_pos[1] + 4 * 64)
        button_ok = Button(interface, ok_onclick, ok_pos, ok_img, ok_hover_img, "ok")
        
        interface.screen.blit(popup_menu.build_image(), menu_draw_pos)
        add_button(interface, button_ok)
    
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
        if any(lvl >= len(levels.ALL_LEVELS) for lvl in userdata.UNLOCKED_LEVELS) and userdata.TUTO_INFO["no_more_levels"]:
            interface.popup_text = strings.get("no_more_levels")
            userdata.TUTO_INFO["no_more_levels"] = False
            userdata.save()
        
        reset_text_img = graphics.RESET_FONT.render("Réinitialiser", True, (70, 70, 70))
        reset_img = pictures.MyImage.void(130, reset_text_img.get_height() + 12)
        reset_img.blit(reset_text_img, ((130 - reset_text_img.get_width()) / 2, 6))
        reset_hover_img = reset_img.copy().highlighted(0.15, 0, 0)
        
        def reset_onclick():
            userdata.reset()
        
        reset_pos = (main.SCREEN_WIDTH - reset_img.get_width() - 10, main.SCREEN_HEIGHT - reset_img.get_height() - 10)
        button_reset = Button(interface, reset_onclick, reset_pos, reset_img, reset_hover_img, "reset")
        add_button(interface, button_reset)
        
        for lvl in range(10):
            lvl_unlocked = levels.is_level_unlocked(lvl)
            
            lvl_img = pictures.MyImage.void(80, 68)
            lvl_text_img = graphics.LEVEL_BUTTON_FONT.render(str(lvl + 1), True, (200,)*3 if lvl_unlocked else (150,)*3)
            
            lvl_img.highlighted(0, 3 if lvl_unlocked else 1, 0.7 if lvl_unlocked else 0.5)
            
            txt_rel_pos = ((lvl_img.get_width() - lvl_text_img.get_width()) / 2, (lvl_img.get_height() - lvl_text_img.get_height()) / 2)
            lvl_img.blit(lvl_text_img, txt_rel_pos)
            
            button_pos = (100 * (lvl % 5) + (main.SCREEN_WIDTH - 480) / 2, 100 * (lvl // 5) + (main.SCREEN_HEIGHT - 200) / 2)
            
            if lvl_unlocked:
                lvl_hover_img = lvl_img.copy().highlighted(0.15, 0, 0)
                
                def lvl_onclick(lvl):
                    def lvl_onclick_():
                        game.GAME_INSTANCE = game.Game(levels.ALL_LEVELS[lvl])
                    return lvl_onclick_
                
                button = Button(interface, lvl_onclick(lvl), button_pos, lvl_img, lvl_hover_img, "lvl" + str(lvl))
            
                add_button(interface, button)
            else:
                interface.screen.blit(lvl_img.build_image(), button_pos)
    
    if time != last_frame:
        interface.screen.blit(graphics.FPS_FONT.render(str(int(1 / (time - last_frame))), True, (150, 0, 200)), (0, 0))
