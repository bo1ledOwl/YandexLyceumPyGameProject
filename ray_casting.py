import pygame
import math
from settings import *


def ray_casting_func(player, map, sc):
    current_angle = player.angle
    xo, yo = player.x, player.y
    for ray in range(NUM_RAYS):
        sin_a = math.sin(current_angle)
        cos_a = math.cos(current_angle)
        x1 = math.tan(current_angle)
        ya = 0
        for depth in range(TILE):
            if yo + depth * sin_a % TILE == 0:
                ya = yo + depth * sin_a
                break
        xa = xo + (ya - yo) / math.tan(current_angle)
        a = 0
        while True:
            if ((xa + x1 * a) // TILE * TILE, (ya + TILE * a) // TILE * TILE) in map.world_map:
                x = xa + x1 * a
                y = ya + TILE * a
                break
            else:
                a += 1
        pygame.draw.line(sc, BLUE, (xo, yo), (x, y), 2)
        current_angle += DELTA_ANGLE
