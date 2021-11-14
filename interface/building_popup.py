import pygame

import pricing
import strings
import userdata
from interface import pictures, graphics, user_interface
from position import Vector2
from towers import castle


def render_popup(interface, game_, time, last_frame, relative_time):
    """
        Dessine le rendu et ajoute les boutons de la popup d'achat et d'amélioration des tours
    :param interface: Interface - l'instance de l'interface
    :param game_: Game - l'instance du jeu
    :param time: nombre - la date actuelle en secondes
    :param last_frame: nombre - la date de la dernière frame
    :param relative_time: nombre - nombre - (la date de cette frame - la date du dernier tick) / la durée d'un tick
    """
    
    # l'image 'top' est au format 8:1
    # l'image 'body' est au format 8:4
    # l'image 'bottom' est au format 8:2
    
    top: pictures.MyImage = pictures.get("top").smoothscaled(True)
    body: pictures.MyImage = pictures.get("body").smoothscaled(True)
    bottom: pictures.MyImage = pictures.get("bottom").smoothscaled(True)
    
    tower = interface.popup_tile.tower
    
    if not tower:
        
        # on affiche 2 tours par ligne
        bodies = (len(game_.level.available_towers) + 1) // 2
        
        popup_img = pictures.MyImage.void(64, 8 + 16 + bodies * 32)
        popup_img.blit(top.scaled_to((64, 8)), (0, 0))
        
        for i in range(bodies):
            popup_img.blit(body.scaled_to((64, 32)), (0, 8 + i * 32))
        
        popup_img.blit(bottom.scaled_to((64, 16)), (0, 8 + bodies * 32))
        
        popup_img.scaled(3)
        
        draw_pos = graphics.get_pixel_pos(interface.popup_tile.position + Vector2(0.5, 0.1), interface) \
                   - Vector2(popup_img.get_width() / 2, popup_img.get_height())
        
        buttons = []
        i = 0
        for tower_type in game_.level.available_towers:
            prices = pricing.tower_prices[tower_type]
            
            def onclick_(tower_type, prices):
                # pour éviter les problèmes de portée des variables, on fait cette étrange chose
                def onclick():
                    if game_.money >= prices[0]:
                        game_.money -= prices[0]
                        interface.popup_tile.tower = tower_type(interface.popup_tile)
                        interface.popup_tile = None
                        if userdata.TUTO_INFO["money"]:
                            interface.popup_text = strings.get("money")
                            userdata.TUTO_INFO["money"] = False
                            userdata.save()
                return onclick

            # le code parle de lui même, difficile d'être plus clair ici
            
            deflation = 0.7

            tower_img = tower_type.get_img(0).scaled_to((32 * 3 * deflation, 32 * 3 * deflation))
            button_pos = (3 * 32 * (i % 2) + draw_pos.x, 3 * 32 * (i // 2) + 8 + draw_pos.y)
            button_pos = (button_pos[0] + 32 * 3 * (1 - deflation) / 2, button_pos[1] + 32 * 3 * (1 - deflation) / 2)
            
            tower_img_hover = tower_img.copy().highlighted(0.2, 2, 0.5)
            buttons.append(user_interface.Button(interface, onclick_(tower_type, prices), button_pos, tower_img, tower_img_hover, "buy" + str(hash(tower_type))))
            
            price_msg = str(prices[0])
            text_img = graphics.PRICES_FONT.render(price_msg, True, (200, 200, 200) if game_.money >= prices[0] else (200, 0, 0))
            text_pos = (3 * 32 * (i % 2) + (3 * 32 - text_img.get_width()) / 2, 3 * 32 * (i // 2 + 1) + 8 - text_img.get_height())
            
            popup_img.blit(text_img, text_pos)
            
            i += 1
        
        graphics.draw_image(interface.screen, draw_pos.to_tuple(), popup_img)
        
        for button in buttons:
            interface.add_button(button)
        
        return popup_img.get_rect().move(*draw_pos.to_tuple())
    
    elif type(tower) is not castle.Castle:
        
        # dessin de la portée de la tour
        circle_radius = tower.shoot_range * graphics.PIXEL_PER_ZOOM * interface.half_zoom
        
        range_circle = pygame.Surface((2 * circle_radius, 2 * circle_radius), pygame.SRCALPHA, 32).convert_alpha()
        pygame.draw.circle(range_circle, (200, 190, 0, 50), (int(circle_radius), int(circle_radius)), circle_radius)
        
        range_circle_draw_pos = (graphics.get_pixel_pos(tower.tile.position.middle() - Vector2(tower.shoot_range, tower.shoot_range), interface))
        interface.screen.blit(range_circle, range_circle_draw_pos.to_tuple())
        
        # dessin de la boite
        popup_img = pictures.MyImage.void(64, 8 + 16 + 32)
        
        popup_img.blit(top.scaled_to((64, 8)), (0, 0))
        popup_img.blit(body.scaled_to((64, 32)), (0, 8))
        popup_img.blit(bottom.scaled_to((64, 16)), (0, 8 + 32))
    
        popup_img.scaled(3)

        button = None

        draw_pos = graphics.get_pixel_pos(interface.popup_tile.position + Vector2(0.5, 0.1), interface) \
                   - Vector2(popup_img.get_width() / 2, popup_img.get_height())
        
        if tower.has_next_level():
            # ajout du bouton d'amélioration
            price = tower.get_next_level_price()
    
            def onclick():
                if game_.money >= price:
                    game_.money -= price
                    tower.level_up()
                    interface.popup_tile = None
    
            lvl_up_img = pictures.get("level_up").scaled(2).smoothscaled(False)
            button_pos = ((3 * 64 - lvl_up_img.get_width()) / 2 + draw_pos.x, 30 + draw_pos.y)
    
            lvl_up_img_hover = lvl_up_img.copy().highlighted(0.2, 2, 0.5)
            button = user_interface.Button(interface, onclick, button_pos, lvl_up_img, lvl_up_img_hover,
                                     "buy" + str(hash(type(tower))))
            
            price_msg = str(price)
            text_img = graphics.PRICES_FONT.render(price_msg, True, (200, 200, 200) if game_.money >= price else (200, 0, 0))
            text_pos = ((3 * 64 - lvl_up_img.get_width()) / 2 + (lvl_up_img.get_width() - text_img.get_width()) / 2, 30 + lvl_up_img.get_height())
            popup_img.blit(text_img, text_pos)
    
        graphics.draw_image(interface.screen, draw_pos.to_tuple(), popup_img)
        
        if button:
            interface.add_button(button)
        
        return popup_img.get_rect().move(*draw_pos.to_tuple())
