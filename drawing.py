import pygame
from ray_casting import ray_casting_func
from settings import *
from math import *
from map import *


class Drawer:
    def __init__(self, surface):
        self.sc = surface
        self.font = pygame.font.SysFont('Arial', 36, bold=True)

    def draw_background(self):
        pygame.draw.rect(self.sc, SKYBLUE, (0, 0, WIDTH, HALF_HEIGHT))
        pygame.draw.rect(self.sc, DARKGRAY, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))

    def draw_minimap(self, player):
        pygame.draw.rect(self.sc, BLACK, (0, 0, world_map[-1][0] * MINIMAP_SCALE, world_map[-1][1] * MINIMAP_SCALE))
        for wall in world_map:
            pygame.draw.rect(self.sc, PURPLE, (wall[0] * MINIMAP_SCALE, wall[1] * MINIMAP_SCALE,
                                               TILE * MINIMAP_SCALE, TILE * MINIMAP_SCALE))
        x, y = player.x, player.y
        pygame.draw.line(self.sc, GREEN, (x * MINIMAP_SCALE, y * MINIMAP_SCALE),
                         ((x + MINIMAP_DEPTH * cos(radians(player.angle))) * MINIMAP_SCALE,
                         (y + MINIMAP_DEPTH * sin(radians(player.angle))) * MINIMAP_SCALE))
        pygame.draw.rect(self.sc, RED,
                         ((x - 15) * MINIMAP_SCALE, (y - 15) * MINIMAP_SCALE, 30 * MINIMAP_SCALE, 30 * MINIMAP_SCALE))

    def fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, True, DARKORANGE)
        self.sc.blit(render, FPS_POS)
