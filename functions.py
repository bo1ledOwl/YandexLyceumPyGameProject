from settings import *
from map import *

def map_coords(x, y):
    return int((x // TILE) * TILE), int((y // TILE) * TILE)

def check_sign(n):
    if n >= 0:
        return 1
    return -1

def check_intersection(x, y, dx, dy, side=WALL_SAFE_RANGE):
    if not map_coords(x + dx + check_sign(dx) * side, y) in world_map:
        x += dx
    if not map_coords(x, y + dy + check_sign(dy) * side) in world_map:
        y += dy
    return x, y
