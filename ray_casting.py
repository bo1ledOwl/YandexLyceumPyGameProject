import pygame
import math
from settings import *
from map import *

def ray_casting_func(player, sc):
    a = (player.angle - HALF_FOV) % 360
    xo, yo = player.x, player.y
    x_on_map, y_on_map = map_coords(xo, yo)
    for ray in range(NUM_RAYS):
        sin_a = math.sin(math.radians(a))
        cos_a = math.cos(math.radians(a))
        if not sin_a:
            sin_a = 0.00000001
        if not cos_a:
            cos_a = 0.00000001

        # по горизонталям
        if sin_a >= 0:
            yh, y_next = y_on_map + TILE, 1
        else:
            yh, y_next = y_on_map, -1
        for _ in range(0, HEIGHT, TILE):
            depth_h = (yh - yo) / sin_a
            xh = xo + depth_h * cos_a
            if map_coords(xh, yh + y_next) in world_map:
                depth_h *= math.cos(math.radians(player.angle - a))
                if depth_h != 0:
                    proj_height_h = PROJECTION_COEFF / depth_h
                break
            yh += y_next * TILE

        # по вертикалям
        if cos_a >= 0:
            xv, x_next = x_on_map + TILE, 1
        else:
            xv, x_next = x_on_map, -1
        for _ in range(0, HEIGHT, TILE):
            depth_v = (xv - xo) / cos_a
            yv = yo + depth_v * sin_a
            if map_coords(xv + x_next, yv) in world_map:
                depth_v *= math.cos(math.radians(player.angle - a))
                if depth_v != 0:
                    proj_height_v = PROJECTION_COEFF / depth_v
                break
            xv += x_next * TILE

        if depth_h < depth_v and depth_h != 0:
            pygame.draw.rect(sc, GREEN, (ray * SCALE, HALF_HEIGHT - proj_height_h // 2, SCALE, proj_height_h))
        elif depth_v < depth_h and depth_v != 0:
            pygame.draw.rect(sc, GREEN, (ray * SCALE, HALF_HEIGHT - proj_height_v // 2, SCALE, proj_height_v))
        a += DELTA_ANGLE