import pygame
import math
from settings import *


def ray_casting_func(player, map, sc):
    current_angle = player.angle
    xo, yo = player.x, player.y
    for ray in range(NUM_RAYS):
        sin_a = math.sin(math.radians(current_angle))
        cos_a = math.cos(math.radians(current_angle))
        x1 = math.tan(math.radians(current_angle))
        if x1 == 0 or cos_a == 0 or sin_a == 0:
            return
        k = 50 / x1
        ya = yo
        xa = xo
        x = xo
        y = yo
        for depth in range(TILE):
            if xo + depth * cos_a % TILE == 0:
                xa = xo + depth * cos_a
                break
        a = 0
        while True:
            if a > 20:
                break
            x_cor = xa + k * a
            if (x_cor // TILE * TILE, (x_cor - xo + yo / x1) * x1 // TILE * TILE) in map.world_map:
                x = x_cor
                y = (x_cor - xo + yo / x1) * x1
                break
            else:
                a += 1
        pygame.draw.line(sc, BLUE, (xo, yo), (x, y), 2)
        current_angle += DELTA_ANGLE
