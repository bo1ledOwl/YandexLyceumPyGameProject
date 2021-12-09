from settings import *
from PIL import Image

world_map = set()
im = Image.open("maps/map.png")
pixels = im.load()
x, y = im.size
WIDTH = x * TILE
HEIGHT = y * TILE
recalculate()
for i in range(x):
    for j in range(y):
        r, g, b = pixels[i, j]
        if (r, g, b) == (0, 0, 0):
            world_map.add((i * TILE, j * TILE))
world_map = sorted(world_map)
