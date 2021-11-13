import random
from copy import deepcopy

import levels
import mobs.mob as mob
import position
import strings
import tiles
import userdata
from interface import ui
from mobs import boss_mob

# les types de dégats
DAMAGE_TYPE_RAW = 0
DAMAGE_TYPE_FIRE = 1
DAMAGE_TYPE_ICE = 2
DAMAGE_TYPE_MAGIC = 3

# ce type existe juste pour infliger des dégats fixes, indépendamment de la résistance des mobs
DAMAGE_TYPE_ABSOLUTE = 4


class Game:
    def __init__(self, level_):
        self._entities = []
        self._level = deepcopy(level_)
        self.money = level_.money
        self._id_inc = 0
        self._wave = 0
        self._just_created = True
        self._btwn_waves = True
        self._next_wave_date = self.current_wave().preparation
        self._game_tick = 0
        self._paused = False
        self._game_beaten = False
        
        if self.level.id == 0 and userdata.TUTO_INFO["basic"]:
            ui.INTERFACE_INSTANCE.popup_text = strings.get("basic1")
            userdata.TUTO_INFO["basic"] = False
            userdata.save()
            userdata.save()
            userdata.save()
            
        if self.level.id == 1 and userdata.TUTO_INFO["controls"]:
            ui.INTERFACE_INSTANCE.popup_text = strings.get("controls")
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
    
    def add_entity(self, entity):
        self._entities.append(entity)
    
    def current_wave(self):
        return self.wave_after(0)
    
    def wave_after(self, n):
        return self.level.waves[(self._wave + n) % len(self.level.waves)]
    
    def tick(self):
        if self.paused or ui.INTERFACE_INSTANCE.popup_text:
            return
        
        self._game_tick += 1
        
        if self._btwn_waves:
            if self._next_wave_date <= self._game_tick:
                self._btwn_waves = False
                if self._just_created:
                    self._just_created = False
                else:
                    self.money += self.current_wave().gift
                    self._wave += 1
                self.current_wave().start(self._game_tick)
        
        elif self.current_wave().is_ended(self._game_tick - 1) and not any((isinstance(ent, boss_mob.BossMob) for ent in self.entities)):
            self._btwn_waves = True
            self._next_wave_date = self._game_tick + self.wave_after(1).preparation
            
        if not self._btwn_waves:
            count_mult = self._wave // len(self.level.waves)
            for mob_type in self.current_wave().next_mobs(self._game_tick) * (1 + count_mult):
                if not mob_type:
                    continue
                health = 5 + self._wave ** 1.5
                
                if mob_type is boss_mob.BossMob:
                    health = self.current_wave().boss_health
                
                shift = position.Position((random.random() - 0.5) * random.random() * 0.7, (random.random() - 0.5) * random.random() * 0.7)
                self.add_entity(mob_type(self, self.level.spawner.position.middle() + shift, health))
        
        for entity in self._entities:
            if entity.is_dead():
                if isinstance(entity, boss_mob.BossMob):
                    levels.unlock_level(self.level.id + 1)
                    ui.INTERFACE_INSTANCE.popup_text = strings.get("win")
                    self._game_beaten = True
                
                self._entities.remove(entity)
            else:
                entity.tick(self._game_tick, self)
        for tower in (tile.tower for tile in self.level.tiles if isinstance(tile, tiles.BuildingTile) and not tile.is_empty()):
            tower.tick(self._game_tick, self)
        
    @property
    def entities(self):
        return self._entities.copy()
    
    @property
    def mobs(self):
        return [amob for amob in self._entities if isinstance(amob, mob.Mob)]
        
    def next_id(self):
        self._id_inc += 1
        return self._id_inc


GAME_INSTANCE: Game = None
