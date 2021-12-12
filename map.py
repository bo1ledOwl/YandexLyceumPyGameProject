from settings import *
from PIL import Image

# соответствие цветов на карте и элементов игры
SPAWN_POINT = (255, 0, 0)
WALL1 = (0, 0, 0)
WALL2 = (100, 100, 100)


def map_coords(x, y):
    return (x // TILE) * TILE, (y // TILE) * TILE


world_map = {}
im = Image.open("maps/map.png")
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
            # красная точка на карте - спавн игрока
            PLAYER_START_POSITION = (i * TILE + TILE // 2, j * TILE + TILE // 2)
