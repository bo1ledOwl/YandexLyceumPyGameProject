import pygame
import math
from settings import *
from map import *


def ray_casting(player, textures):
    a = (player.angle - HALF_FOV) % 360
    xo, yo = player.x, player.y
    x_on_map, y_on_map = map_coords(xo, yo)
    objects = {}
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
        for _ in range(0, MAP_HEIGHT, TILE):
            depth_h = (yh - yo) / sin_a
            xh = xo + depth_h * cos_a
            coords = map_coords(xh, yh + y_next)
            if coords in world_map:
                depth_h *= math.cos(math.radians(player.angle - a))
                texture_h = textures[world_map[coords]]
                if depth_h == 0:
                    depth_h = 0.00001
                proj_height_h = int(PROJECTION_COEFF / depth_h)
                break
            yh += y_next * TILE

        # по вертикалям
        if cos_a >= 0:
            xv, x_next = x_on_map + TILE, 1
        else:
            xv, x_next = x_on_map, -1
        for _ in range(0, MAP_WIDTH, TILE):
            depth_v = (xv - xo) / cos_a
            yv = yo + depth_v * sin_a
            coords = map_coords(xv + x_next, yv)
            if coords in world_map:
                depth_v *= math.cos(math.radians(player.angle - a))
                texture_v = textures[world_map[coords]]
                if depth_v == 0:
                    depth_v = 0.00001
                break
            xv += x_next * TILE

        if depth_h < depth_v:
            depth, offsetX, proj_height, texture = (depth_h, int(xh) % TILE, int(PROJECTION_COEFF / depth_h), texture_h)
        else:
            depth, offsetX, proj_height, texture = (depth_v, int(yv) % TILE, int(PROJECTION_COEFF / depth_v), texture_v)
        wall = texture.subsurface(offsetX * TEXTURE_SCALE, 0, TEXTURE_SCALE, TEXTURE_HEIGHT)
        wall = pygame.transform.scale(wall, (SCALE, proj_height))
        objects[ray] = ((depth, wall, (ray * SCALE, HALF_HEIGHT - proj_height / 2)))
        a += DELTA_ANGLE
        a %= 360
    return objects
