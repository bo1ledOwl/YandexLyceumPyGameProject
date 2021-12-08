import pygame
from ray_casting import ray_casting_func
from settings import *
from math import *


class Drawer:
    def __init__(self, surface, map):
        self.sc = surface
        self.map = map

    def draw_player(self, player):
        x, y = player.x, player.y
        pygame.draw.rect(self.sc, RED, (x - 15, y - 15, 30, 30))
        pygame.draw.line(self.sc, GREEN, (x, y), (x + MAX_DEPTH * cos(radians(player.angle)), y - MAX_DEPTH * sin(radians(player.angle))))

    def draw_map(self):
        for wall in self.map.world_map:
            pygame.draw.rect(self.sc, DARKGRAY, (wall[0], wall[1], TILE, TILE))
