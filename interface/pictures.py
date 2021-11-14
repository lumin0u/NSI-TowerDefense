import math
from os import listdir
from os.path import isfile, join
import re
import random
import time

import pygame
from PIL import Image, ImageSequence

from interface import graphics

RANDOM_HASH = random.randint(-2**63, 2**63-1)

# données pour les animations
_EXTRA_DATA = eval(open("resources/images/animations.json", mode='r').read())


# https://www.py4u.net/discuss/14105
def pilImageToSurface(pilImage):
    mode, size, data = pilImage.mode, pilImage.size, pilImage.tobytes()
    return pygame.image.frombuffer(data, size, mode)#.convert_alpha()


# https://www.py4u.net/discuss/14105
def load_gif(filename):
    pilImage = Image.open(filename)
    frames = []
    if pilImage.format == 'GIF' and pilImage.is_animated:
        for frame in ImageSequence.Iterator(pilImage):
            pygameImage = pilImageToSurface(frame.convert('RGBA'))
            frames.append(pygameImage)
    else:
        frames.append(pilImageToSurface(pilImage))
    return frames


def get_frame(img, time_, animation_delay):
    """
        Retourne la frame à l'instant 'time_' du gif 'img' quand un frame dure 'animation_delay' secodnes
    :param img: list[T] - le gif
    :param time_: nombre - la date actuelle
    :param animation_delay: nombre - la durée en secondes d'une frame pour ce gif
    :return: T - l'image à l'instant 'time_'
    """
    total_length = len(img) * animation_delay
    time_ %= total_length
    accumulator = 0
    for frame in img:
        if animation_delay + accumulator > time_:
            return frame
        accumulator += animation_delay


class Picture:
    """
        Représente les rendus que peuvent prendre une image
        Un object Picture peut n'être qu'une image ou un gif
        Cette classe, a contrario de MyImage, est immutable
    """
    def __init__(self, name, directory=""):
        """
        :param name: nom du fichier de l'image, sans l'extension
        :param directory: dossier où se trouve l'image (avec "/" à la fin)
        """
        self._possible_images = []
        self._name = name
        
        directory_path = "resources/images/" + directory
        self._directory_path = directory_path
        
        # on parcours tout les fichiers dans le dossier
        for file in [f for f in listdir(directory_path) if isfile(join(directory_path, f))]:
            # si le fichier sans l'extension a le même nom que l'image, on l'ajoute aux images
            if re.fullmatch(name + "(\\$\\d+)?\\.\\w+", file):
                if file.endswith("gif"):
                    self._possible_images.append((directory + file, load_gif(directory_path + file)))
                else:
                    self._possible_images.append((directory + file, pygame.image.load(directory_path + file)))
        
        if len(self._possible_images) == 0:
            raise RuntimeError("Missing resource for image " + name)
    
    def get_img(self, pseudo_random=0):
        """
            Retourne le rendu actuel de l'image représentée à l'instant actuel
        :param pseudo_random: nombre - un nombre pseudo aléatoire pour le choix de l'image
        :return: le rendu actuel de l'image
        """
        file, img = self._possible_images[(pseudo_random ^ RANDOM_HASH) % len(self._possible_images)]
        
        if type(img) is list:
            # gif
            surface = get_frame(img, time.time(), _EXTRA_DATA[file]["speed"])
        else:
            surface = img.copy()
        
        return MyImage(surface)
        

class MyImage:
    """
        Représente une image
        Cette classe permet d'apporter des modifications successives à une image en ne faisant les calculs qu'au moment\
        du dessin, ce qui permet par exemple d'améliorer les performances en ne redimmensionnant l'image qu'une seule \
        fois quand la méthode scale() a été appelée plusieurs fois, ou de ne pas perdre de qualité
    """
    def __init__(self, image):
        """
        :param image: Surface - l'image de base
        """
        self._image = image
        
        # les actions à éxécuter à la construction de l'image sont stockées dans ce dictionnaire
        self._actions = {"scale": (1, 1), "highlight": (0, 0, 0), "fade": 1, "rotation": 0, "blits": [],
                         "scale_to": None}
        
        # multiplicateur final de la taille
        self._final_scale = (1, 1)
        self.smoothscaling = True
    
    def _scale_it(self, image, size):
        """
            Redimensionne l'image en utilisant la fonction (scale ou smoothscale) adapté à cet objet
        :param image: Surface - l'image à redimensionner
        :param size: tuple - (width, height) les dimensions de l'image
        :return: Surface - l'image redimensionnée
        """
        if self.smoothscaling:
            return pygame.transform.smoothscale(image, size)
        else:
            return pygame.transform.scale(image, size)
    
    def build_image(self):
        """
            Construit l'image et la retourne, c'est-à-dire applique toutes les actions à effectuer
        :return:
        """
        scale = self._actions["scale"]
        scale_to = self._actions["scale_to"]
        fade = self._actions["fade"]
        angle = self._actions["rotation"]
        blits = self._actions["blits"]

        new_size = (self._image.get_width(), self._image.get_height())
        
        if scale_to:
            new_size = scale_to

        new_size = (int(new_size[0] * scale[0]), int(new_size[1] * scale[1]))
        
        # on évite de redimensionner une image à ses dimensions
        if new_size != (self._image.get_width(), self._image.get_height()):
            self._image = self._scale_it(self._image, new_size)
        
        if fade != 1:
            self._image.fill((255, 255, 255, int(fade * 255)), special_flags=pygame.BLEND_RGBA_MULT)
        
        if angle != 0:
            size = self._image.get_width() * self._image.get_height()
            self._image = pygame.transform.rotate(self._image, angle)
            r_size = math.sqrt(self._image.get_width() * self._image.get_height() / size)
            self.final_scaled(r_size)
        
        for image, position, _ in blits:
            self._image.blit(image.build_image(), position)
        
        self._actions = {"scale": (1, 1), "scale_to": None, "highlight": (0, 0, 0), "fade": 1, "rotation": 0, "blits": []}
        return self._image
    
    @property
    def final_scale(self):
        return self._final_scale
    
    def scaled(self, scale):
        """
            Redimensionne l'image en multipliant ses dimensions par un facteur soit unique soit propre à chaque \
            dimension
        :param scale: tuple | nombre - multiplie les dimensions par ce facteur
        :return: MyImage - self
        """
        if type(scale) is int or type(scale) is float:
            self._actions["scale"] = (self._actions["scale"][0] * scale, self._actions["scale"][1] * scale)
            # redimensionnement et replacement des images à dessiner
            for tup in self._actions["blits"]:
                tup[0].scaled(scale)
                tup[1] = (tup[1][0] * scale, tup[1][1] * scale)
        elif type(scale) is tuple:
            self._actions["scale"] = (self._actions["scale"][0] * scale[0], self._actions["scale"][1] * scale[1])
            # redimensionnement et replacement des images à dessiner
            for tup in self._actions["blits"]:
                tup[0].scaled(scale)
                tup[1] = (tup[1][0] * scale[0], tup[1][1] * scale[1])
        return self
    
    def scaled_to(self, size):
        """
            Redimensionne l'image aux dimensions données
        :param size: tuple - (width, height) les nouvelles dimensions
        :return: MyImage - self
        """
        self._actions["scale"] = (1, 1)
        self._actions["scale_to"] = size

        # redimensionnement et replacement des images à dessiner
        for tup in self._actions["blits"]:
            tup[0].scaled_to((size[0] * tup[0].get_width() / self._image.get_width(), size[1] * tup[0].get_height() / self._image.get_height()))
            tup[1] = (tup[2][0] / self._image.get_width() * size[0], tup[2][1] / self._image.get_height() * size[1])
        return self
    
    def final_scaled(self, scale):
        """
            Redimensionnement final de l'image à la manière de scale()
            Valable uniquement pour les images apparaissant dans le jeu, c'est-à-dire les tuiles, les tours et les mobs
        :param scale: tuple | nombre - multiplie les dimensions par ce facteur
        :return: MyImage - self
        """
        if type(scale) is int or type(scale) is float:
            self._final_scale = (self._final_scale[0] * scale, self._final_scale[1] * scale)
        elif type(scale) is tuple:
            self._final_scale = (self._final_scale[0] * scale[0], self._final_scale[1] * scale[1])
        return self
    
    def highlighted(self, highlight_alpha, border_width, border_alpha):
        """
        :return: MyImage - self
        """
        self._image = graphics.highlight(self._image, highlight_alpha, border_width, border_alpha)
        return self
    
    def faded(self, alpha):
        """
            Diminue la valeur du canal alpha de toute l'image
        :param alpha: nombre - dans [0; 1] la valeur maximale dans le canal alpha
        :return: MyImage - self
        """
        self._actions["fade"] -= (1 - alpha) * self._actions["fade"]
        for img, pos in self._actions["blits"]:
            img.faded(alpha)
        return self
    
    def rotated(self, angle):
        """
            Tourne l'image de 'angle' degrés et adapte la taille finale de l'image
        :param angle: nombre - l'angle exprimé en degrés
        :return: MyImage - self
        """
        self._actions["rotation"] += angle
        return self
    
    def blit(self, surface, pos=(0, 0)):
        """
            Dessine l'image donnée à la position donnée
        :param surface: MyImage | Surface - l'image à dessiner
        :param pos: tuple - (x, y) le coin haut gauche de l'image, par défaut: (0, 0)
        :return: MyImage - self
        """
        self._actions["blits"].append([(surface if isinstance(surface, MyImage) else MyImage(surface)).copy(), pos, pos])
        return self
    
    def get_width(self):
        """
        :return: nombre - la largeur de l'image, altérée par les modification de redimensionnement
        """
        if self._actions["scale_to"]:
            return self._actions["scale_to"][0]
        return self._image.get_width() * self._actions["scale"][0]
    
    def get_height(self):
        """
        :return: nombre - la hauteur de l'image, altérée par les modification de redimensionnement
        """
        if self._actions["scale_to"]:
            return self._actions["scale_to"][1]
        return self._image.get_height() * self._actions["scale"][1]
    
    def get_rect(self):
        """
        :return: Rect - le rectangle de l'image, altéré par les modification de redimensionnement
        """
        return pygame.Rect(0, 0, self.get_width(), self.get_height())
    
    def copy(self):
        """
        :return: MyImage - une copie de cet objet, en conservant les actions à effectuer
        """
        copy_ = MyImage(self._image.copy())
        copy_._actions = self._actions.copy()
        copy_._final_scale = self._final_scale
        return copy_
    
    def smoothscaled(self, value):
        """
            Définit si l'image doit être redimensionnée à l'aide de la fonction 'smoothscale' ou 'scale' du
            module pygame
        :param value: bool - est-ce que l'image doit être redimensionnée à l'aide de la fonction 'smoothscale'
        :return: MyImage - self
        """
        self.smoothscaling = value
        return self
    
    @staticmethod
    def void(width, height):
        """
            Retourne une image de dimensions données complétement transparente
        :param width: nombre - la largeur de l'image
        :param height: nombre - la hauteur de l'image
        :return: MyImage - l'image générée
        """
        return MyImage(pygame.Surface((width, height), pygame.SRCALPHA, 32).convert_alpha())


# stockage des images chargées
PICTURES = {}


def load_pictures():
    """
        Charge toutes les images du jeu
    """
    load_picture("building_tile")
    load_picture("spawner")
    load_picture("path_NE")
    load_picture("path_WE")
    
    load_picture("volume_0", "buttons/")
    load_picture("volume_1", "buttons/")
    load_picture("volume_2", "buttons/")
    load_picture("level_up", "buttons/")
    load_picture("pause", "buttons/")
    
    load_picture("simple_tower", "towers/")
    load_picture("castle", "towers/")
    load_picture("explosive_tower", "towers/")
    load_picture("sniper_tower", "towers/")
    load_picture("freeze_tower", "towers/")

    load_picture("dart", "projectiles/")
    load_picture("shell", "projectiles/")
    
    load_picture("carre", "mobs/")
    load_picture("robuste", "mobs/")
    load_picture("example_mob", "mobs/")
    load_picture("boss", "mobs/")
    load_picture("triangle", "mobs/")
    
    for i in range(14):
        load_picture("health" + str(i), "mobs/")

    load_picture("top", "tower_popup/")
    load_picture("body", "tower_popup/")
    load_picture("bottom", "tower_popup/")


def load_picture(name, directory=""):
    PICTURES[name] = Picture(name, directory)


def get(name, pseudo_random=0):
    """
    :return: MyImage - l'image de nom 'name'
    """
    return PICTURES[name].get_img(pseudo_random)
