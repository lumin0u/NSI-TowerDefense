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
from position import Position, Vector2
import interface.graphics as graphics
from interface import game_render


def lerp(a, b, delta):
    """
        Pour 'linear interpolation', retourne l'interpolation linéaire entre a et b
    :param a: {__mul__}
    :param b: {__mul__}
    :param delta: nombre - généralement compris dans l'intervalle [0; 1], si m = 0, a est retourné, si m = 1, b est \
     retourné
    :return: l'interpolation linéaire entre a et b
    """
    delta = max(0, min(1, delta))
    return b * delta + a * (1 - delta)


def _aroundrandom(scale):
    """
    :return: nombre - une valeur aléatoire choisie selon une loi non uniforme dans l'intervalle [-scale; scale[
    """
    return random.random() * (random.random() * scale - scale / 2)


class Interface:
    """
        Représente l'interface du programme
        Il ne doit exister qu'une seule instance de la classe Interface tout au long de l'éxécution
    """
    def __init__(self, screen):
        global INTERFACE_INSTANCE
        INTERFACE_INSTANCE = self
        
        self._screen: pygame.Surface = screen
        self.volume = 0
        self.buttons = []
        
        # information sur l'endroit où l'utilisateur à commencé son clic
        self._click_start = "free"
        
        # popup pour l'achat et l'amélioration d'une tour
        self.popup_tile: tiles.Tile = None
        self.popup_rect: pygame.Rect = None
        
        #
        self.background_shade = 0
        
        # les particules à dessiner, une particule suit le schéma suivant
        # [0:position initiale, 1:position finale, 2:angle initial, 3:angle final, 4:taille, 5:age,
        # 6:vitesse d'animation, 7:durée de vie, 8:nom de la particule]
        self.smokes = []
        
        # lignes de texte de la notification, une valeur à None indique qu'il n'y a pas de notification à afficher
        self.popup_text: list[str] = None
        # popup_button_action est une fonction à appeler en plus de la fermeture de la notification lors de la pression\
        # sur le bouton OK
        self.popup_button_action = None
        
        # position en jeu de la caméra
        self.camera_pos = Position(0, 0)
        # position de la caméra entre deux instants pour un mouvement fluide
        self._half_camera_pos = self.camera_pos

        # niveau de zoom
        self.zoom = 2
        # niveau de zoom entre deux instants pour un mouvement fluide
        self._half_zoom = 1 / 100

    def new_smoke(self, position, scale=1., dir_: Union[tuple, float, int] = 50, randomizer=0.5, speed=5, lifetime=2, img_name="smoke"):
        """
            Ajoute une particule à dessiner
        :param position: tuple - (x, y) la position de la particule
        :param scale: nombre - le multiplicateur de la taille de la particule, par défaut: 1
        :param dir_: tuple | nombre - (x, y) un tuple représente la direction et la longueur du trajet de la particule
            un nombre indique la longueur du trajet et la direction et choisie aléatoirement, par défaut: 50
            la longueur est exprimée en tuiles
        :param randomizer: nombre - taux d'aléatoire dans le trajet de la particule, par défaut: 0.5
        :param speed: nombre - vitesse de l'animation, par défaut: 5
        :param lifetime: nombre - age maximal en secondes, par défaut: 2 secondes
        :param img_name: str - nom de la particule, par défaut: "smoke"
        :return: list - la particule qui est ajoutée
        """
        if dir_ and type(dir_) is tuple:
            rand_angle = random.random() * 2 * math.pi
            angle = math.atan2(dir_[1], dir_[0])
            dir_change = (1 + _aroundrandom(randomizer))
            dir_ = math.sqrt(dir_[0] ** 2 + dir_[1] ** 2) * dir_change
            angle += math.atan(_aroundrandom(randomizer)) / dir_change
            x = math.cos(angle) * dir_
            y = math.sin(angle) * dir_
            smoke = [position, (x, y), random.random() * 360, random.random() * 720 - 360, scale, 0, speed, lifetime, img_name]
        else:
            dir_ = float(dir_) * (1 + _aroundrandom(randomizer))
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
        """
            Recalcule les zoom et position de caméra pour donner un mouvement fluide
        :param delta: nombre - temps écoulé depuis la dernière frame
        """
        self._half_zoom = lerp(self.half_zoom, self.zoom, delta * 15)
        self._half_camera_pos = lerp(self.half_camera_pos, self.camera_pos, delta * 15)
    
    def mouse_down(self, mouse_button, mouse_pos):
        """
            Méthode appelée lorsqu'un bouton de la souris est pressé
        :param mouse_button: inutilisé
        :param mouse_pos: inutilisé
        """
        # si l'utilisateur appuie sur un bouton, on actualise la variable click_start
        for button in self.buttons:
            if button.rect.move(button.position).collidepoint(pygame.mouse.get_pos()):
                self._click_start = button.id
                return
        self._click_start = "free"
    
    def mouse_up(self, game_, mouse_button, mouse_pos):
        """
            Méthode appelée lorsqu'un bouton de la souris est relâché
        :param game_: Game - l'instance du jeu
        :param mouse_button: inutilisé
        :param mouse_pos: inutilisé
        """
        if not self.popup_tile or not self.popup_rect or not self.popup_rect.collidepoint(pygame.mouse.get_pos()):
            # s'il n'existe pas de popup d'achat ou d'amélioration de tour, ou que l'utilisateur clique à coté de
            # celle-ci
            
            # on ferme la popup si elle existe
            self.popup_tile = None
            self.popup_rect = None
            
            # on itère les boutons pour savoir s'il clique sur l'un
            for button in self.buttons:
                if button.id == self._click_start and button.rect.move(button.position).collidepoint(pygame.mouse.get_pos()):
                    button.onclick()
                    return
            
            # sinon on itère les tuiles pour potentiellement ouvrir une popup d'achat ou d'amélioration de tour
            if game_:
                for tile in game_.level.tiles:
                    if tile.is_clickable() and tile.get_on_screen_rect(self).collidepoint(pygame.mouse.get_pos()):
                        self.popup_tile = tile
        else:
            # si la popup d'achat ou d'amélioration de tour existe, on regarde si l'utilisateur clique sur un de ses
            # boutons
            for button in self.buttons:
                if button.id == self._click_start \
                        and button.rect.move(button.position).collidepoint(pygame.mouse.get_pos()) \
                        and button.id.startswith("buy"):
                    button.onclick()
                    return
    
    def is_clicking_button(self, button):
        """
        :param button: Button - le bouton à tester
        :return: bool - est-ce que l'utilisateur est en train de cliquer sur ce bouton
        """
        return pygame.mouse.get_pressed(3)[0] and self._click_start == button.id

    def render(self, game_, time, last_frame, relative_time):
        """
            Dessine le rendu d'une frame
        :param game_: Game - l'instance du jeu ou None
        :param time: nombre - la date actuelle en secondes
        :param last_frame: nombre - la date de la dernière frame
        :param relative_time: nombre - (la date de cette frame - la date du dernier tick) / la durée d'un tick
        """
        if game_ and game_.game_beaten:
            # affichage de l'arrière-plan en une teinte de vert si le boss est vaincu
            pygame.draw.rect(self.screen, (0, 40 * self.background_shade, 0), (0, 0, main.SCREEN_WIDTH, main.SCREEN_HEIGHT))
            if self.background_shade < 1:
                self.background_shade += 0.001
        else:
            # arrière-plan en noir sinon
            pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, main.SCREEN_WIDTH, main.SCREEN_HEIGHT))
            self.background_shade = 0
        
        self.buttons = []
        main.clear_hand_reasons()
    
        delta = time - last_frame
        
        # déplacement de la caméra à l'aide des touches zqsd et des flèches
        if pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_z]:
            self.camera_pos += Vector2(0, -8 * delta / math.sqrt(self.zoom))
        if pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_s]:
            self.camera_pos += Vector2(0, 8 * delta / math.sqrt(self.zoom))
        if pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_q]:
            self.camera_pos += Vector2(-8 * delta / math.sqrt(self.zoom), 0)
        if pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]:
            self.camera_pos += Vector2(8 * delta / math.sqrt(self.zoom), 0)
            
        self.update_halves(delta)
        
        if game_:
            # l'affichage des éléments du jeu sont gérés dans le module game_redner
            game_render.render_game(self, game_, time, last_frame, relative_time)
            
            if game_.paused:
                # en pause, l'affichage du jeu est foncé
                self.screen.fill((100, 100, 100), special_flags=pygame.BLEND_MULT)
        else:
            # s'il n'y a pas de jeu en cours, on remet les valeurs de position de caméra et de zoom par défaut
            self.camera_pos = Position(0, 0)
            self.zoom = 2
            self._half_zoom = 1 / 100
        
        # affichage de l'interface utilisateur
        self.show_ui(game_, time, last_frame, relative_time)
    
        for smoke in self.smokes:
            # on retire les particules mortes
            if smoke[5] > smoke[7]:
                self.smokes.remove(smoke)
                continue
            # et on dessine les vivantes
            graphics.draw_particle(self, smoke, time - last_frame)
        
        # fin des dessins
        # mise à jour de l'écran
        pygame.display.update()
    
    def add_button(self, button):
        """
            Ajoute un bouton à la liste des boutons disponibles pour cette frame
        :param button: Button - le bouton à ajouter
        """
        if pygame.rect.Rect(button.rect.move(button.position)).collidepoint(
                pygame.mouse.get_pos()):
            # si la souris survole le bouton, il est affiché différemment et le curseur devient une main
            graphics.draw_image(self.screen, button.position, button.hover_img)
            main.set_hand_reason("hover_button_" + str(hash(button.id)), True)
        else:
            graphics.draw_image(self.screen, button.position, button.img)
            main.set_hand_reason("hover_button_" + str(hash(button.id)), False)
        
        self.buttons.append(button)
    
    def show_ui(self, game_, time, last_frame, relative_time):
        """
            Dessine et ajoute les boutons de l'interface utilisateur, c'est-à-dire les boutons tels que la pause ou le \
            changement de volume, la boite de notification, le menu pause et les choix de niveaux s'il n'y a pas de \
            partie en cours
        :param game_: Game - l'instance du jeu
        :param time: nombre - la date actuelle en secondes
        :param last_frame: nombre - la date de la dernière frame
        :param relative_time: nombre - (la date de cette frame - la date du dernier tick) / la durée d'un tick
        """
        if not game_ or game_.paused:
            # le bouton de volume est affiché s'il n'y a pas de partie en cours ou que le jeu est en pause
            
            volume_img = pictures.get("volume_" + str(self.volume))
            volume_hover_img = volume_img.copy().highlighted(0.15, 0, 0)
            
            def volume_onclick():
                self.volume = (self.volume - 1) % 3
                pygame.mixer.music.set_volume((self.volume / 4) ** 2)
            
            button = Button(self, volume_onclick, (10, main.SCREEN_HEIGHT - volume_img.get_height() - 10), volume_img, volume_hover_img, "volume")
            self.add_button(button)
        
        if self.popup_text:
            # affichage de la notification
            
            # l'image 'top' est au format 8:1
            # l'image 'body' est au format 8:4
            
            # création de la boite
            popup_menu = pictures.MyImage.void(4 * 64, 4 * (2 * 8 + 2 * 32))
            popup_menu.blit(pictures.get("top").scaled_to((4 * 64, 4 * 8)), (0, 0))
            popup_menu.blit(pictures.get("body").scaled_to((4 * 64, 4 * 32)), (0, 4 * 8))
            popup_menu.blit(pictures.get("body").scaled_to((4 * 64, 4 * 32)), (0, 4 * (8 + 32)))
            # on ne prend pas l'image 'bottom' mais l'image 'top' retournée
            popup_menu.blit(pictures.get("top").scaled_to((4 * 64, 4 * 8)).rotated(180), (0, 4 * (8 + 2 * 32)))
            
            menu_draw_pos = ((main.SCREEN_WIDTH - 4 * 64) / 2, (main.SCREEN_HEIGHT - 4 * (2 * 8 + 2 * 32)) / 2)
            
            # décalage en pixels du haut de la boite
            line_offset = 20
            
            # rendu du message ligne par ligne
            for line in self.popup_text:
                # le rendu des lignes vides n'est pas calculé mais le saut de ligne est pris en compte
                if line and line != "":
                    text_img = graphics.INFO_FONT.render(line, True, (255, 255, 255, 127))
                    
                    text_pos = ((popup_menu.get_width() - text_img.get_width()) // 2, int(line_offset))
                    popup_menu.blit(text_img, text_pos)
    
                line_offset += graphics.INFO_FONT.get_height() * 1.5
            
            # ajout du bouton OK
            ok_text_img = graphics.PAUSE_BUTTONS_FONT.render("OK", True, (255, 255, 255, 127))
            ok_img = pictures.MyImage.void(70, ok_text_img.get_height() + 12)
            ok_img.blit(ok_text_img, ((70 - ok_text_img.get_width()) / 2, 6))
            
            ok_img.highlighted(0.15, 2, 0.6)
            ok_hover_img = ok_img.copy().highlighted(0.15, 0, 0)
            
            def ok_onclick():
                # lors du clic sur le bouton OK, on ferme la notification et on éxécute l'action supplémentaire si
                # elle est définie
                self.popup_text = None
                action = self.popup_button_action
                self.popup_button_action = None
                if action:
                    action()
            
            ok_pos = (menu_draw_pos[0] + 160, menu_draw_pos[1] + 4 * 64)
            button_ok = Button(self, ok_onclick, ok_pos, ok_img, ok_hover_img, "ok")
            
            self.screen.blit(popup_menu.build_image(), menu_draw_pos)
            self.add_button(button_ok)
        
        if game_:
            # ---- EN JEU ----
            
            # ajout du bouton pause
            pause_img = pictures.get("pause")
            pause_hover_img = pause_img.copy().highlighted(0.15, 0, 0)
            
            def pause_onclick():
                game_.paused = not game_.paused
            
            button_pause = Button(self, pause_onclick, (20, 20), pause_img, pause_hover_img, "pause")
            self.add_button(button_pause)
            
            if game_.paused:
                # si le jeu est en pause, on affiche le menu de pause
                
                # voir plus haut pour des explications sur la boite
                pause_menu = pictures.MyImage.void(4 * 64, 4 * (2 * 8 + 2 * 32))
                pause_menu.blit(pictures.get("top").scaled_to((4 * 64, 4 * 8)), (0, 0))
                pause_menu.blit(pictures.get("body").scaled_to((4 * 64, 4 * 32)), (0, 4 * 8))
                pause_menu.blit(pictures.get("body").scaled_to((4 * 64, 4 * 32)), (0, 4 * (8 + 32)))
                pause_menu.blit(pictures.get("top").scaled_to((4 * 64, 4 * 8)).rotated(180), (0, 4 * (8 + 2 * 32)))
                
                menu_draw_pos = ((main.SCREEN_WIDTH - 4 * 64) / 2, (main.SCREEN_HEIGHT - 4 * (2 * 8 + 2 * 32)) / 2)
                
                # ajout du bouton 'Reprendre'
                resume_text_img = graphics.PAUSE_BUTTONS_FONT.render("Reprendre", True, (255, 255, 255, 127))
                resume_img = pictures.MyImage.void(215, resume_text_img.get_height() + 12)
                resume_img.blit(resume_text_img, ((215 - resume_text_img.get_width()) / 2, 6))
                
                resume_img.highlighted(0.15, 2, 0.6)
                resume_hover_img = resume_img.copy().highlighted(0.15, 0, 0)
                
                def resume_onclick():
                    game_.paused = False
                
                resume_pos = (menu_draw_pos[0] + 20, menu_draw_pos[1] + 4 * 8 + 40)
                button_resume = Button(self, resume_onclick, resume_pos, resume_img, resume_hover_img, "resume")
                
                # ajout du bouton 'Quitter'
                leave_text_img = graphics.PAUSE_BUTTONS_FONT.render("Quitter", True, (255, 255, 255, 127))
                leave_img = pictures.MyImage.void(215, leave_text_img.get_height() + 12)
                leave_img.blit(leave_text_img, ((215 - leave_text_img.get_width()) / 2, 6))
                
                leave_img.highlighted(0.15, 2, 0.6)
                leave_hover_img = leave_img.copy().highlighted(0.15, 0, 0)
                
                def leave_onclick():
                    game.GAME_INSTANCE = None
                
                leave_pos = (menu_draw_pos[0] + 20, menu_draw_pos[1] + 4 * 8 + 4 * 32 + 40)
                button_leave = Button(self, leave_onclick, leave_pos, leave_img, leave_hover_img, "leave")
                
                # dessin de la boite PUIS ajout des boutons
                self.screen.blit(pause_menu.build_image(), menu_draw_pos)
                self.add_button(button_resume)
                self.add_button(button_leave)
        else:
            # ---- AU MENU ----
            
            # affichage d'une notification indiquant qu'il n'y a pas plus de niveaux si des niveaux inexistant
            # sont débloqués
            if any(lvl >= len(levels.ALL_LEVELS) for lvl in userdata.UNLOCKED_LEVELS) and userdata.TUTO_INFO["no_more_levels"]:
                self.popup_text = strings.get("no_more_levels")
                userdata.TUTO_INFO["no_more_levels"] = False
                userdata.save()
            
            # ajout du bouton 'Réinitialiser'
            reset_text_img = graphics.RESET_FONT.render("Réinitialiser", True, (70, 70, 70))
            reset_img = pictures.MyImage.void(130, reset_text_img.get_height() + 12)
            reset_img.blit(reset_text_img, ((130 - reset_text_img.get_width()) / 2, 6))
            reset_hover_img = reset_img.copy().highlighted(0.15, 0, 0)
            
            def reset_onclick():
                userdata.reset()
            
            reset_pos = (main.SCREEN_WIDTH - reset_img.get_width() - 10, main.SCREEN_HEIGHT - reset_img.get_height() - 10)
            button_reset = Button(self, reset_onclick, reset_pos, reset_img, reset_hover_img, "reset")
            self.add_button(button_reset)
            
            # ajout des boutons pour chaque niveau
            for lvl in range(10):
                
                # l'affichage du bouton est différent si le niveau est débloqué ou non
                lvl_unlocked = levels.is_level_unlocked(lvl)
                
                lvl_img = pictures.MyImage.void(80, 68)
                lvl_text_img = graphics.LEVEL_BUTTON_FONT.render(str(lvl + 1), True, (200, 200, 200) if lvl_unlocked else (150, 150, 150))
                
                lvl_img.highlighted(0, 3 if lvl_unlocked else 1, 0.7 if lvl_unlocked else 0.5)
                
                txt_rel_pos = ((lvl_img.get_width() - lvl_text_img.get_width()) / 2, (lvl_img.get_height() - lvl_text_img.get_height()) / 2)
                lvl_img.blit(lvl_text_img, txt_rel_pos)
                
                button_pos = (100 * (lvl % 5) + (main.SCREEN_WIDTH - 480) / 2, 100 * (lvl // 5) + (main.SCREEN_HEIGHT - 200) / 2)
                
                if lvl_unlocked:
                    lvl_hover_img = lvl_img.copy().highlighted(0.15, 0, 0)
                    
                    def lvl_onclick(lvl):
                        # pour éviter les problèmes de portée des variables, on fait cette étrange chose
                        def lvl_onclick_():
                            game.GAME_INSTANCE = game.Game(levels.ALL_LEVELS[lvl])
                        return lvl_onclick_
                    
                    button = Button(self, lvl_onclick(lvl), button_pos, lvl_img, lvl_hover_img, "lvl" + str(lvl))
                
                    self.add_button(button)
                else:
                    # si le niveau est bloqué, l'image est dessiné sans qu'elle soit un bouton
                    self.screen.blit(lvl_img.build_image(), button_pos)
        
        if time != last_frame:
            # affichage des fps en violet
            self.screen.blit(graphics.FPS_FONT.render(str(int(1 / (time - last_frame))), True, (150, 0, 200)), (0, 0))


# l'instance unique de l'interface, dans une variable globale
INTERFACE_INSTANCE: Interface = None


class Button:
    """
        Représente un bouton
        Une instance de bouton n'existe que pour une frame (elle n'est en tout cas sauvegardé que ce temps-là)
    """
    
    def __init__(self, interface, onclick, position, img, hover_img, id_):
        """
        :param interface: Interface - l'instance de l'interface
        :param onclick: function - la fonction a appeler lors du clic sur le bouton
        :param position: Position - la position du bouton
        :param img: MyImage - l'image du bouton avant le clic ou le survol
        :param hover_img: MyImage - l'image du bouton lors du survol
        :param id_: str - l'identifiant unique du bouton. 2 boutons ne peuvent avoir le même id lors d'une même frame,\
            c'est cependant possible sur 2 frames différentes
        """
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