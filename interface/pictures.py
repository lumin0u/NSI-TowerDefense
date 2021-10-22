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
        self._final_size = (1, 1)
    
    def final_image(self):
        return self._image
    
    @property
    def final_size(self):
        return self._final_size
    
    def scaled(self, scale):
        new_size = (int(self._image.get_width() * scale), int(self._image.get_height() * scale))
        self._image = pygame.transform.smoothscale(self._image, new_size)
        return self
    
    def scaled_to(self, size):
        self._image = pygame.transform.smoothscale(self._image, size)
        return self
    
    def final_scaled(self, scale):
        self._final_size = (self._final_size[0] * scale, self._final_size[1] * scale)
        return self
    
    def highlighted(self, highlight_alpha, border_width, border_alpha):
        self._image = graphics.highlight(self._image, highlight_alpha, border_width, border_alpha)
        return self
    
    def shaded(self, alpha):
        self._image.fill((255, 255, 255, int(alpha * 255)), special_flags=pygame.BLEND_RGBA_MULT)
        return self
    
    def blit(self, surface):
        if isinstance(surface, MyImage):
            self._image.blit(surface.final_image(), (0, 0))
        else:
            self._image.blit(surface, (0, 0))
    
    def get_height(self):
        return self._image.get_height()
    
    def get_width(self):
        return self._image.get_width()
    
    def get_rect(self):
        return self._image.get_rect()
    
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
    load_picture("carre", "mobs/")
    load_picture("robuste", "mobs/")
    load_picture("example_mob", "mobs/")
    load_picture("boss", "mobs/")


def load_picture(name, directory=""):
    PICTURES[name] = Picture(name, directory)
