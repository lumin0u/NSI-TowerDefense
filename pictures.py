from os import listdir
from os.path import isfile, join
import re
import pygame
from PIL import Image, ImageSequence


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


def get_frame(img, time):
    total_length = len(img) * 0.1
    time %= total_length
    accumulator = 0
    for frame in img:
        if 0.1 + accumulator > time:
            return frame
        accumulator += 0.1


class Picture:
    def __init__(self, name, directory=""):
        self._possible_images = []
        
        directory_path = "images/" + directory
        
        for file in [f for f in listdir(directory_path) if isfile(join(directory_path, f))]:
            if re.fullmatch(name + "(\\$\\d+)?\\.\\w+", file):
                if file.endswith("gif"):
                    self._possible_images.append(load_gif(directory_path + file))
                else:
                    self._possible_images.append(pygame.image.load(directory_path + file))
        
        if len(self._possible_images) == 0:
            raise RuntimeError("Missing resource for image " + name)
    
    def get_img(self, time, tile_position):
        """
            merci de n'utiliser que cette méthode
        """
        img = self._possible_images[0] if tile_position is None else self._image_from_position(tile_position)
        
        if type(img) is list:
            return get_frame(img, time)
        return img.copy()

    def _image_from_position(self, tile_position):
        return self._possible_images[hash(tile_position) % len(self._possible_images)]


PICTURES = {}


def load_pictures():
    load_picture("building_tile")
    load_picture("mouse_hover")
    load_picture("spawner")
    load_picture("path_NE")
    load_picture("path_WE")


def load_picture(name, directory=""):
    PICTURES[name] = Picture(name, directory)
