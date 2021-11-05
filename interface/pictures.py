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

_EXTRA_DATA = eval(open("images/animations.json", mode='r').read())


def pilImageToSurface(pilImage):
    mode, size, data = pilImage.mode, pilImage.size, pilImage.tobytes()
    return pygame.image.frombuffer(data, size, mode)#.convert_alpha()


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


def get_frame(img, time, animation_delay):
    total_length = len(img) * animation_delay
    time %= total_length
    accumulator = 0
    for frame in img:
        if animation_delay + accumulator > time:
            return frame
        accumulator += animation_delay


class Picture:
    def __init__(self, name, directory=""):
        self._possible_images = []
        self._name = name
        
        directory_path = "images/" + directory
        self._directory_path = directory_path
        
        for file in [f for f in listdir(directory_path) if isfile(join(directory_path, f))]:
            if re.fullmatch(name + "(\\$\\d+)?\\.\\w+", file):
                if file.endswith("gif"):
                    self._possible_images.append((directory + file, load_gif(directory_path + file)))
                else:
                    self._possible_images.append((directory + file, pygame.image.load(directory_path + file)))
        
        if len(self._possible_images) == 0:
            raise RuntimeError("Missing resource for image " + name)
    
    def get_img(self, pseudo_random=0):
        """
            merci de n'utiliser que cette méthode
        """
        file, img = self._possible_images[(pseudo_random ^ RANDOM_HASH) % len(self._possible_images)]
        
        if type(img) is list:
            surface = get_frame(img, time.time(), _EXTRA_DATA[file]["speed"])
        else:
            surface = img.copy()
        
        return MyImage(surface)
        

class MyImage:
    def __init__(self, image: pygame.Surface):
        self._image = image
        self._actions = {"scale": (1, 1), "scale_to": None, "highlight": (0, 0, 0), "shade": 1, "rotation": 0, "blits": []}
        self._final_size = (1, 1)
        self.smoothscaling = True
    
    def _scale_it(self, image, size):
        if self.smoothscaling:
            return pygame.transform.smoothscale(image, size)
        else:
            return pygame.transform.scale(image, size)
    
    def build_image(self):
        scale = self._actions["scale"]
        scale_to = self._actions["scale_to"]
        shade = self._actions["shade"]
        angle = self._actions["rotation"]
        blits = self._actions["blits"]
        
        if scale_to:
            self._image = self._scale_it(self._image, scale_to)
        
        new_size = (int(self._image.get_width() * scale[0]), int(self._image.get_height() * scale[1]))
        self._image = self._scale_it(self._image, new_size)

        self._image.fill((255, 255, 255, int(shade * 255)), special_flags=pygame.BLEND_RGBA_MULT)
        
        size = self._image.get_width() * self._image.get_height()
        self._image = pygame.transform.rotate(self._image, angle)
        r_size = math.sqrt(self._image.get_width() * self._image.get_height() / size)
        self.final_scaled(r_size)
        
        for image, position in blits:
            if isinstance(image, MyImage):
                self._image.blit(image.build_image(), position)
            else:
                self._image.blit(image, position)
        
        self._actions = {"scale": (1, 1), "scale_to": None, "highlight": (0, 0, 0), "shade": 1, "rotation": 0, "blits": []}
        return self._image
    
    @property
    def final_size(self):
        return self._final_size
    
    def scaled(self, scale):
        if type(scale) is int or type(scale) is float:
            self._actions["scale"] = (self._actions["scale"][0] * scale, self._actions["scale"][1] * scale)
        elif type(scale) is tuple:
            self._actions["scale"] = (self._actions["scale"][0] * scale[0], self._actions["scale"][1] * scale[1])
        return self
    
    def scaled_to(self, size):
        self._actions["scale"] = (1, 1)
        self._actions["scale_to"] = size
        return self
    
    def final_scaled(self, scale):
        if type(scale) is int or type(scale) is float:
            self._final_size = (self._final_size[0] * scale, self._final_size[1] * scale)
        elif type(scale) is tuple:
            self._final_size = (self._final_size[0] * scale[0], self._final_size[1] * scale[1])
        return self
    
    def highlighted(self, highlight_alpha, border_width, border_alpha):
        """self._actions["highlight"] =
        self._actions.append(("highlight", (highlight_alpha, border_width, border_alpha)))"""
        self._image = graphics.highlight(self._image, highlight_alpha, border_width, border_alpha)
        return self
    
    def shaded(self, alpha):
        self._actions["shade"] -= (1 - alpha) * self._actions["shade"]
        return self
    
    def rotated(self, angle):
        self._actions["rotation"] += angle
        return self
    
    def blit(self, surface, pos=(0, 0)):
        self._actions["blits"].append((surface, pos))
    
    def get_width(self):
        if self._actions["scale_to"]:
            return self._actions["scale_to"][0]
        return self._image.get_width() * self._actions["scale"][0]
    
    def get_height(self):
        if self._actions["scale_to"]:
            return self._actions["scale_to"][1]
        return self._image.get_height() * self._actions["scale"][1]
    
    def get_rect(self):
        return pygame.Rect(0, 0, self.get_width(), self.get_height())
    
    def copy(self):
        return MyImage(self._image.copy())


PICTURES = {}


def load_pictures():
    load_picture("building_tile")
    load_picture("spawner")
    load_picture("path_NE")
    load_picture("path_WE")
    
    load_picture("volume_0", "buttons/")
    load_picture("volume_1", "buttons/")
    load_picture("volume_2", "buttons/")
    
    load_picture("simple_tower", "towers/")
    load_picture("castle", "towers/")
    load_picture("explosive_tower", "towers/")
    
    load_picture("carre", "mobs/")
    load_picture("robuste", "mobs/")
    load_picture("example_mob", "mobs/")
    load_picture("boss", "mobs/")
    
    for i in range(14):
        load_picture("health" + str(i), "mobs/")

    load_picture("dart", "projectiles/")
    load_picture("shell", "projectiles/")


def load_picture(name, directory=""):
    PICTURES[name] = Picture(name, directory)
