import os
from settings import *
from PIL import Image

# соответствие цветов на карте и элементов игры
SPAWN_POINT = (0, 255, 0)  # точка появления
ENEMIES = [(50, 0, 0), (100, 0, 0), (150, 0, 0), (200, 0, 0)]
OBJECTS = [(0, 0, 50), (0, 0, 100)]
# виды стен
WALLS = [(0, 0, 0), (50, 50, 50), (100, 100, 100), (200, 200, 200)]
DOORS = [(150, 150, 150)]

world_map = {}
enemies_coords = {}
objects_coords = {}
im = Image.open(os.path.join("resources/maps/map.png"))
pixels = im.load()
x, y = im.size
MAP_WIDTH = x * TILE
MAP_HEIGHT = y * TILE
for i in range(x):
    for j in range(y):
        r, g, b = pixels[i, j]
        if (r, g, b) in WALLS:
            world_map[(i * TILE, j * TILE)] = str(WALLS.index((r, g, b)))
        if (r, g, b) in DOORS:
            world_map[(i * TILE, j * TILE)] = 'd' + str(DOORS.index((r, g, b)))
        if (r, g, b) == SPAWN_POINT:
            PLAYER_START_POSITION = (i * TILE + TILE // 2, j * TILE + TILE // 2)
        if (r, g, b) in ENEMIES:
            enemies_coords[(i * TILE, j * TILE)] = ENEMIES.index((r, g, b))
        if (r, g, b) in OBJECTS:
            objects_coords[(i * TILE, j * TILE)] = OBJECTS.index((r, g, b))
