import pygame
from ray_casting import ray_casting_func
from settings import *
from math import *
from map import *


class Drawer:
    def __init__(self, surface):
        self.sc = surface

    def draw_background(self):
        pygame.draw.rect(self.sc, DARKGRAY, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT * 0.55))

    def draw_minimap(self, player):
        for wall in world_map:
            pygame.draw.rect(self.sc, SKYBLUE, (wall[0] * MINIMAP_SCALE, wall[1] * MINIMAP_SCALE, TILE * MINIMAP_SCALE, TILE * MINIMAP_SCALE))
        x, y = player.x, player.y
        pygame.draw.rect(self.sc, RED, ((x - 15) * MINIMAP_SCALE, (y - 15) * MINIMAP_SCALE, 30 * MINIMAP_SCALE, 30 * MINIMAP_SCALE))
        pygame.draw.line(self.sc, GREEN, (x * MINIMAP_SCALE, y * MINIMAP_SCALE),
        ((x + MINIMAP_DEPTH * cos(radians(player.angle))) * MINIMAP_SCALE, (y + MINIMAP_DEPTH * sin(radians(player.angle))) * MINIMAP_SCALE))
