import random
from copy import deepcopy

import levels
import mobs.mob as mob
import position
import strings
import tiles
import userdata
from interface import user_interface
from mobs import boss_mob

# les types de dégats
DAMAGE_TYPE_RAW = 0
DAMAGE_TYPE_FIRE = 1
DAMAGE_TYPE_ICE = 2
DAMAGE_TYPE_MAGIC = 3

# ce type existe juste pour infliger des dégats fixes, indépendamment de la résistance des mobs
DAMAGE_TYPE_ABSOLUTE = 4


class Game:
    """
        Représente une partie, définie par un niveau
        Une partie commence au choix du niveau et se finit quand le joueur perd ou qu'il retourne au menu
    """
    def __init__(self, level):
        """
        :param level: Level - le niveau
        """
        self._entities = []
        self._level = deepcopy(level)
        self.money = level.money
        
        # un nombre qui est incrémenté à chaque création d'entité, ce qui permet l'obtention d'un id unique pour chaque
        self._id_inc = 0
        
        # wave est un nombre - le numéro de la vague - et pas un objet de type Wave
        self._wave = 0
        
        self._just_created = True
        self._btwn_waves = True
        
        # next_wave_date est la date du début de la prochaine vague et est exprimée en ticks
        self._next_wave_date = self.current_wave().preparation
        
        self._game_tick = 0
        self._paused = False
        
        # est-ce que le joueur a tué au moins un boss cette partie
        self._game_beaten = False
        
        # le tutoriel n'est affiché qu'une seule fois
        # le principe du jeu est expliqué au niveau 1
        if self.level.id == 0 and userdata.TUTO_INFO["basic"]:
            user_interface.INTERFACE_INSTANCE.popup_text = strings.get("basic1")
            userdata.TUTO_INFO["basic"] = False
            userdata.save()

        # les controles au niveau 2, car inutiles au niveau 1
        if self.level.id == 1 and userdata.TUTO_INFO["controls"]:
            user_interface.INTERFACE_INSTANCE.popup_text = strings.get("controls")
            userdata.TUTO_INFO["controls"] = False
            userdata.save()
    
    @property
    def level(self):
        return self._level
    
    @property
    def game_beaten(self):
        return self._game_beaten
    
    @property
    def wave(self):
        return self._wave
    
    @property
    def game_tick(self):
        return self._game_tick
    
    @property
    def btwn_waves(self):
        return self._btwn_waves
    
    @property
    def next_wave_date(self):
        return self._next_wave_date
    
    @next_wave_date.setter
    def next_wave_date(self, value):
        self._next_wave_date = value
    
    @property
    def paused(self):
        return self._paused
    
    @paused.setter
    def paused(self, value):
        self._paused = value
        
        interface = user_interface.INTERFACE_INSTANCE
        if interface.popup_text:
            if interface.popup_button_action:
                interface.popup_button_action()
            interface.popup_text = None
            interface.popup_button_action = None
    
    def add_entity(self, entity):
        """
            Ajoute une entité à la liste des entités à prendre en compte
        :param entity: Entity - l'entité à ajouter
        """
        self._entities.append(entity)
    
    def current_wave(self):
        """
            Retourne la vague actuelle, selon self._wave
            Si la vague dépasse le nombre de vagues existantes, la vague actuelle modulo le nombre de vagues \
            est retournée
        :return: Wave - la vague actuelle
        """
        return self.wave_after(0)
    
    def wave_after(self, n):
        """
            Retourne la vague self._wave + n soit la vague après n vagues
            Si la vague dépasse le nombre de vagues existantes, la vague actuelle modulo le nombre de vagues \
            est retournée
            Une valeur négative de n est autorisée.
        :param n: nombre - le nombre de vagues à ignorer
        :return: Wave - la vague après n vagues
        """
        return self.level.waves[(self._wave + n) % len(self.level.waves)]
    
    def tick(self):
        """
            Impulsion du jeu, appelée à un rythme régulier, prédéfini dans le module main
            Tout les calculs relatifs au déroulement du jeu sont effectués lors d'un tick
            La classe Game transmet l'impulsion de tick aux entités et aux tours
        """
        if self.paused or user_interface.INTERFACE_INSTANCE.popup_text:
            return
        
        self._game_tick += 1
        
        # entre deux vagues
        if self._btwn_waves:
            if self._next_wave_date <= self._game_tick:
                # si la date de la prochaine vague est dépassée, elle commence et on offre le revenu de la vague
                self._btwn_waves = False
                if self._just_created:
                    self._just_created = False
                else:
                    self.money += self.current_wave().gift
                    self._wave += 1
                self.current_wave().start(self._game_tick)
        
        elif self.current_wave().is_ended(self._game_tick - 1) and not any((isinstance(ent, boss_mob.BossMob) for ent in self.entities)):
            # si la vague est en cours, que tout les mobs sont apparus et qu'il ne reste plus de boss en vie
            # la vague se finit et la prochaine se prépare
            self._btwn_waves = True
            self._next_wave_date = self._game_tick + self.wave_after(1).preparation
        
        if not self._btwn_waves:
            # si il y a une vague en cours
            
            # si la vague courante dépasse le nombre de vagues existantes, plus de mobs apparaissent
            count_mult = self._wave // len(self.level.waves)
            
            # on itère les mobs qui doivent apparaitre à ce tick
            for mob_type in self.current_wave().next_mobs(self._game_tick) * (1 + count_mult):
                if not mob_type:
                    continue
                
                health = 5 + self._wave ** 1.5
                
                # les boss ont une vie fixe définie dans la vague
                if mob_type is boss_mob.BossMob:
                    health = self.current_wave().boss_health
                
                shift = position.Position((random.random() - 0.5) * random.random() * 0.7, (random.random() - 0.5) * random.random() * 0.7)
                
                self.add_entity(mob_type(self, self.level.spawner.position.middle() + shift, health))
        
        for entity in self._entities:
            # les entitées mortes sont retirées
            if entity.is_dead():
                # si le boss est tué, la partie est gagnée
                # si le boss meurt dû aux dégats qu'inflige le chateau, le message indiquant la défaite apparaitra avant
                # l'éxécution de ce code
                if isinstance(entity, boss_mob.BossMob):
                    levels.unlock_level(self.level.id + 1)
                    user_interface.INTERFACE_INSTANCE.popup_text = strings.get("win")
                    self._game_beaten = True
                
                self._entities.remove(entity)
            else:
                entity.tick(self._game_tick, self)
        
        for tile in self.level.tiles:
            if isinstance(tile, tiles.BuildingTile) and not tile.is_empty():
                tile.tower.tick(self._game_tick, self)
        
    @property
    def entities(self):
        return self._entities.copy()
    
    @property
    def mobs(self):
        return [amob for amob in self._entities if isinstance(amob, mob.Mob)]
        
    def next_id(self):
        self._id_inc += 1
        return self._id_inc


# l'instance du jeu est stockée dans une variable globale pour être accessible tout le temps
# il n'est sensé y avoir qu'une seule instance de Game à tout instant de l'éxécution
GAME_INSTANCE = None
