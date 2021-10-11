from os import listdir
from os.path import isfile, join
import re
import random

import pygame
from PIL import Image, ImageSequence

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
    
    def get_img(self, time, pseudo_random=0):
        """
            merci de n'utiliser que cette méthode
        """
        file, img = self._possible_images[(pseudo_random ^ RANDOM_HASH) % len(self._possible_images)]
        
        if type(img) is list:
            return get_frame(img, time, _EXTRA_DATA[file]["speed"])
        return img.copy()


PICTURES = {}


def load_pictures():
    load_picture("building_tile")
    load_picture("spawner")
    load_picture("path_NE")
    load_picture("path_WE")


def load_picture(name, directory=""):
    PICTURES[name] = Picture(name, directory)
