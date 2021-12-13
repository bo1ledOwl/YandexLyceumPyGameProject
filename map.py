import os
from settings import *
from PIL import Image


def map_coords(x, y):
    return (x // TILE) * TILE, (y // TILE) * TILE


# соответствие цветов на карте и элементов игры
SPAWN_POINT = (255, 0, 0) # точка появления
# виды стен
WALL1 = (0, 0, 0)
WALL2 = (100, 100, 100)

world_map = {}
im = Image.open(os.path.join("resources/maps/map.png"))
pixels = im.load()
x, y = im.size
MAP_WIDTH = x * TILE
MAP_HEIGHT = y * TILE
for i in range(x):
    for j in range(y):
        r, g, b = pixels[i, j]
        if (r, g, b) == WALL1:
            world_map[(i * TILE, j * TILE)] = 1
        if (r, g, b) == WALL2:
            world_map[(i * TILE, j * TILE)] = 2
        if (r, g, b) == SPAWN_POINT:
            PLAYER_START_POSITION = (i * TILE + TILE // 2, j * TILE + TILE // 2)
