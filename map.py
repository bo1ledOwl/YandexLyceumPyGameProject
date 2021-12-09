from settings import *
from PIL import Image


def map_coords(x, y):
    return (x // TILE) * TILE, (y // TILE) * TILE


world_map = set()
im = Image.open("maps/map.png")
pixels = im.load()
x, y = im.size
MAP_WIDTH = x * TILE
MAP_HEIGHT = y * TILE
for i in range(x):
    for j in range(y):
        r, g, b = pixels[i, j]
        if (r, g, b) == (0, 0, 0):
            world_map.add((i * TILE, j * TILE))
        if (r, g, b) == (255, 0, 0):
            # красная точка на карте - спавн игрока
            PLAYER_START_POSITION = (i * TILE + TILE // 2, j * TILE + TILE // 2)
world_map = sorted(world_map)
