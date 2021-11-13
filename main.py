import time

import pygame

import pricing
import levels
import game
import listener
from interface import pictures, ui, graphics
from mobs import simple_mob, robuste_mob, boss_mob, quick_mob
from towers import simple_tower, explosive_tower, sniper_tower, freeze_tower

# ces variables ne sont pas des constantes, elles peuvent être modifiées par un event de type VIDEO_RESIZE
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

# constante: la durée en secondes d'un tick (normalement 0.05)
TICK_REAL_TIME = 0.05

# ~constantes: ces dictionnaires permettent de récupérer la classe d'un mob ou d'une tour depuis leur nom
TOWERS_NAMES = {
    "simple": simple_tower.SimpleTower,
    "explosive": explosive_tower.ExplosiveTower,
    "sniper": sniper_tower.SniperTower,
    "freeze": freeze_tower.FreezeTower
}
MOBS_NAMES = {
    "simple": simple_mob.SimpleMob,
    "robuste": robuste_mob.RobusteMob,
    "boss": boss_mob.BossMob,
    "rapide": quick_mob.QuickMob
}


def set_hand_reason(reason, value):
    """
        Défini si la souris doit apparaitre en main pour une clé donnée
        La souris apparait en main si au moins une clé est à True
    :param reason: str - la clé
    :param value: bool - si la souris doit apparaitre en main ou en pointeur
    """
    graphics.cursor_hand_reasons[reason] = value


def clear_hand_reasons():
    """
        Retire toutes les clés, la souris apparait par défaut en pointeur
    """
    graphics.cursor_hand_reasons.clear()
    

def main():
    # initialisation de pygame
    pygame.init()
    
    # chargement des modules qui en ont besoin
    pictures.load_pictures()
    levels.build_levels()
    pricing.load()
    graphics.load_fonts()
    
    # initialisation de la fenêtre, redimensionnable
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags=pygame.RESIZABLE)
    
    interface = ui.Interface(screen)
    interface.volume = 0
    
    last_frame = time.time()
    last_tick = time.time()
    
    # chargement du module de son de pygame et lancement de la musique
    pygame.mixer.init()
    # les copyrights de cette musique nous permettent de l'utiliser
    pygame.mixer.music.load("resources/musics/HOME - Resting State - 14.mp3")
    pygame.mixer.music.play(1000)
    pygame.mixer.music.set_volume((interface.volume / 4) ** 2)
    
    # boucle principale
    while True:
        if time.time() > TICK_REAL_TIME + last_tick:
            # s'il y a une instance du jeu en cours, lui impulser un tick
            if game.GAME_INSTANCE:
                game.GAME_INSTANCE.tick()
                last_tick = time.time()
        
        this_frame = time.time()
        
        # affichage de l'interface et du jeu
        ui.render(interface, game.GAME_INSTANCE, this_frame, last_frame, min(1., (this_frame - last_tick) / TICK_REAL_TIME))
        
        # si une des clés est à True, le curseur apparait en main
        if any((v for v in graphics.cursor_hand_reasons.values())):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        # sinon en pointeur
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        # les events de pygame sont gérés dans le module listener
        for event in pygame.event.get():
            listener.catch_event(event, interface)
        
        last_frame = this_frame


if __name__ == '__main__':
    main()
