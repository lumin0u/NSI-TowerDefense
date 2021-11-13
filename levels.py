import math
import random
from copy import copy

import main
import userdata
from mobs import boss_mob
import tiles
from position import TilePosition, Direction


class Wave:
    """
        Représente une vague, l'objet en lui-même peut être réutilisé, mais doit être réinitialisé avant utilisation
    """
    def __init__(self, preparation, mobs_, gift, boss_health=0):
        """
        :param preparation: int - temps en ticks de préparation à la vague
        :param mobs_: dictionnaire - {classe du mob: nombre d'apparitions}
        :param gift: nombre - argent gagné à la fin de la vague
        :param boss_health: nombre - vie du boss, ignorer si la vague n'en contient pas
        """
        self._preparation = preparation
        self._mobs = mobs_
        self._gift = gift
        self._scheduler = {}
        
        self.start_date = 0
        self._boss_health = boss_health
    
    @property
    def preparation(self):
        return self._preparation
    
    @property
    def boss_health(self):
        return self._boss_health
    
    @property
    def gift(self):
        return self._gift
    
    def start(self, start_date):
        """
            Marque le début de la vague et précise quels mobs appairaitront à chaque ticks
        :param start_date: int - date en ticks du début de la vague
        """
        # scheduler: {date en ticks: liste de mobs}
        # contient, pour chaque date où au moins un mob apparait, la liste des mobs qui apparaissent à cette date
        self._scheduler = {}
        self.start_date = start_date
        
        # buffer est une copie de mobs, ce qui permet de modifier buffer sans altérer la structure de la vague
        # pour les prochaines utilisations
        buffer = copy(self._mobs)
        
        # si la vague fait apparaitre au moins un boss, c'est une vague boss
        # il est retiré de buffer car le boss apparait à la fin
        boss_wave = boss_mob.BossMob in buffer and buffer[boss_mob.BossMob]
        if boss_wave:
            buffer[boss_mob.BossMob] = 0
        
        # on stocke le mob qui apparait le plus dans cette vague
        max_mob_count = max((v for v in self._mobs.values()))
        for mob in buffer:
            # l'algorithme suivant permet de choisir à quels dates apparaitront des instances de mob
            # celui-ci va avancer par période de temps aléatoires pour placer ces instances par date
            
            i = 0
            time = 0
            
            while buffer[mob] > 0:
                # ces trois valeurs altèrent la période de temps entre deux apparitions
                # r1 est une constante
                r1 = 24
                
                # r2 permet de faire des 'vagues dans la vague' à l'aide de la fonction sinus
                r2 = (math.sin(i) * 0.8 + 0.9) ** 2
                
                # r3 premet de réguler les mobs moins présents dans la vague, de manière à ce qu'ils n'apparaissent
                # pas tous dans les premières secondes
                r3 = max_mob_count / self._mobs[mob]
                
                # la période est comprise entre 2 et 40 ticks
                time += min(40, max(2, int(random.random() * r1 * r2 * r3)))
                # on ajoute aussi de l'aléatoire non altéré
                time += random.randint(0, 4)
                
                if time not in self._scheduler:
                    self._scheduler[time] = []
                self._scheduler[time].append(mob)
                
                # il reste un mob de moins a faire apparaitre
                buffer[mob] -= 1
                
                i += 1
        
        if boss_wave:
            # le boss apparait toujours 80 ticks (4 secondes) après tout les autres mobs
            self._scheduler[max(self._scheduler.keys()) + 80] = [boss_mob.BossMob]
    
    def is_ended(self, current_tick):
        """
            Dit s'il reste des mobs à faire apparaitre après le tick current_tick ou non
        :param current_tick: int - le tick actuel, ou pas
        :return: bool - si la vague est terminé au tick current_tick
        """
        return not any((k > current_tick - self.start_date for k in self._scheduler))
    
    def next_mobs(self, current_tick):
        """
            Retourne la liste des mobs à faire apparaitre au tick current_tick, ou une liste vide s'il n'y en a aucun
        :param current_tick: int - le tick actuel, ou pas
        :return: list[Mob] - Les mobs à faire apparaitre au tick current_tick
        """
        if current_tick - self.start_date in self._scheduler:
            return self._scheduler[current_tick - self.start_date]
        return []


class Level:
    """
        Représente un niveau, celui-ci contient toutes les tuiles présentes sur ce niveau, l'argent possédé au début \
        de de celui-ci, les points de vie du chateau et les vagues
    """
    def __init__(self, id_, spawner, castle, money, tiles_, waves, available_towers):
        """
        :param id_: int - numéro du niveau, unique
        :param spawner: SpawnerTile - la tuile d'apparition des mobs
        :param castle: CastleTile - la tuile du chateau
        :param money: int - l'argent possédé au début du niveau
        :param tiles_: list[Tile] - toutes les autres tuiles de ce niveau, soit les tuiles constructibles et les \
            chemins.
        :param waves: list[Wave] - la liste des vagues
        :param available_towers: list[type] - la liste des tours disponibles pour ce niveau
        """
        self._spawner = spawner
        self._castle = castle
        self._tiles: list[tiles.Tile] = [self._spawner, self._castle] + tiles_.copy()
        self._waves: list[Wave] = waves.copy()
        self._money = money
        self._available_towers = available_towers
        self._id = id_
    
    def tile_at(self, position):
        """
            Retourne la tuile à cette position. S'il n'y en a aucune, retourne une EmptyTile
        :param position: Position | TilePosition - la position où rechercher une tuile
        :return: Tile - la tuile à la position position
        """
        # on recherche dans nos tuiles s'il en existe une a cette position
        for tile in self._tiles:
            if tile.position == TilePosition.of(position):
                return tile
        
        # s'il n'en existe pas, on en créé une vide
        return tiles.EmptyTile(TilePosition.of(position))
    
    @property
    def tiles(self):
        return self._tiles
    
    @property
    def waves(self) -> list:
        return self._waves
    
    @property
    def spawner(self):
        return self._spawner
    
    @property
    def castle(self):
        return self._castle
    
    @property
    def money(self):
        return self._money
    
    @property
    def available_towers(self):
        return self._available_towers

    @property
    def id(self):
        return self._id


# tout les niveaux, chargés dans build_levels()
ALL_LEVELS = ()


def cardinal_to_direction(s):
    """
    :param s: str - "S", "N", "E" ou "W" pour South, North, Est, West
    :return: Direction - la direction équivalente
    """
    return {"S": Direction(0, 1), "N": Direction(0, -1), "E": Direction(1, 0), "W": Direction(-1, 0)}[s]


# pour avoir un nom plus court
ctd = cardinal_to_direction


def build_levels():
    """
        Construit les niveaux depuis les fichiers json en ressources
    """
    global ALL_LEVELS

    # le json est parfaitement interprétable en python
    # levels_json: [0: chemin d'accès au fichier contenant les données du niveau 0, 1: ...]
    levels_json = eval(open("resources/levels/levels.json", mode="r").read())
    
    levels_list = []
    
    for lvl_id in range(len(levels_json)):
        # le json est parfaitement interprétable en python
        level = eval(open("resources/levels/" + levels_json[lvl_id], mode="r").read())
        
        """
        Le chemin des mobs - et donc la position et direction des tuiles de chemins, de spawner et de chateau -
        sont définis par une chaine de caractères représentant des directions.
        La position du spawner est donnée par ses coordonnées x et y
        Par exemple, "SEE" signifie que le chemin partira du spawner, descendra, ira à droite une fois, puis atteindra
        le chateau.
        Schéma:
        
        S
        P P C
        
        S: spawner, C: chateau, P: tuile chemin
        """
        path_current = TilePosition.of(level["spawner"])
        
        spawner = tiles.SpawnerTile(path_current, ctd(level["path"][0]))
        tiles_ = []
        
        for i in range(len(level["path"]) - 1):
            path_current += ctd(level["path"][i])
            tiles_.append(tiles.PathTile(path_current, -ctd(level["path"][i]), ctd(level["path"][i + 1])))
            
        path_current += ctd(level["path"][-1])
        castle = tiles.CastleTile(path_current, level["castle_health"])
        
        money = level["money"]
        
        for tower_slot in level["tower_slots"]:
            tiles_.append(tiles.BuildingTile(TilePosition.of(tower_slot)))
        
        waves = []
        
        for wave in level["waves"]:
            # les noms simplifiés ("boss", "simple", ...) sont convertis en leur classe (BossMob, SimpleMob, ...)
            mobs = {main.MOBS_NAMES[k]: v for k, v in wave["mobs"].items()}
            boss_health = wave["boss_health"] if "boss_health" in wave else 0
            waves.append(Wave(wave["preparation"], mobs, wave["gift"], boss_health))

        # les noms simplifiés ("explosive", "sniper", ...) sont convertis en leur classe (ExplosiveTower,
        # SniperTower, ...)
        authorized_towers = [main.TOWERS_NAMES[name] for name in level["towers"]]
        
        levels_list.append(Level(lvl_id, spawner, castle, money, tiles_, waves, authorized_towers))
    
    ALL_LEVELS = tuple(levels_list)


def is_level_unlocked(level):
    """
        Indique si le niveau level est débloqué ou non
    :param level: int - le niveau
    :return: bool - si le niveau est débloqué
    """
    return level in userdata.UNLOCKED_LEVELS


def unlock_level(level):
    """
        Débloque le niveau level et le sauvegarde dans le ficher de données
    :param level: int - le niveau
    """
    userdata.UNLOCKED_LEVELS.append(level)
    userdata.save()
