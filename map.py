from PIL import Image
from settings import *


class Map:
    def __init__(self, map_image):
        im = Image.open(map_image)
        self.pixels = im.load()  # список с пикселями
        self.x, self.y = im.size  # ширина (x) и высота (y) изображения
        self.text_map = [['.' for a in range(self.x)] for b in range(self.y)]
        self.world_map = set()
        self.set_maps()


    def set_maps(self):
        for i in range(self.y):
            for j in range(self.x):
                r, g, b = self.pixels[j, i]
                if (r, g, b) == (0, 0, 0):
                    self.text_map[i][j] = '#'
                else:
                    self.text_map[i][j] = '.'

        for j, row in enumerate(self.text_map):
            for i, char in enumerate(row):
                if char != '.':
                    if char == '#':
                        self.world_map.add((i * 50, j * 50))
        self.world_map = sorted(self.world_map)
