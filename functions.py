from settings import *
from map import *

def map_coords(x, y):
    return int((x // TILE) * TILE), int((y // TILE) * TILE)

def check_sign(n):
    if n >= 0:
        return 1
    return -1

def check_intersection(x, y, dx, dy):
    if not map_coords(x + dx + check_sign(dx) * WALL_SAFE_RANGE, y) in world_map:
        x += dx
    if not map_coords(x, y + dy + check_sign(dy) * WALL_SAFE_RANGE) in world_map:
        y += dy
    return x, y
