import math
import os.path
import pygame
import player
from ray_casting import ray_casting
from settings import *
from math import *
from map import world_map


class Drawer:
    def __init__(self, surface):
        self.sc = surface
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        self.textures = {1: pygame.image.load(os.path.join('resources/walls/wall1.png')).convert(),
                         2: pygame.image.load(os.path.join('resources/walls/wall2.png')).convert(),
                         }

    def background(self):
        pygame.draw.rect(self.sc, SKYBLUE, (0, 0, WIDTH, HALF_HEIGHT))
        pygame.draw.rect(self.sc, DARKGRAY, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))

    def world(self, objects, player):
        walls = ray_casting(player, self.textures)
        for obj in sorted(list(walls.values()) + list(map(lambda obj: obj.locate(walls), objects)), key=lambda a: a[0], reverse=True):
            if obj[0]:
                self.sc.blit(obj[1], obj[2])

    def minimap(self, player):
        pygame.draw.rect(self.sc, BLACK, (0, 0, list(world_map.keys())[-1][0] * MINIMAP_SCALE, list(world_map.keys())[-1][1] * MINIMAP_SCALE))
        for wall in world_map:
            pygame.draw.rect(self.sc, PURPLE, (wall[0] * MINIMAP_SCALE, wall[1] * MINIMAP_SCALE,
                                               TILE * MINIMAP_SCALE, TILE * MINIMAP_SCALE))
        x, y = player.x, player.y
        pygame.draw.line(self.sc, GREEN, (x * MINIMAP_SCALE, y * MINIMAP_SCALE),
                         ((x + MINIMAP_DEPTH * cos(radians(player.angle))) * MINIMAP_SCALE,
                         (y + MINIMAP_DEPTH * sin(radians(player.angle))) * MINIMAP_SCALE))
        pygame.draw.rect(self.sc, RED,
                         ((x - 15) * MINIMAP_SCALE, (y - 15) * MINIMAP_SCALE, 60 * MINIMAP_SCALE, 60 * MINIMAP_SCALE))
        # квадратик тестового объекта
        pygame.draw.rect(self.sc, YELLOW,
                         (19 * TILE * MINIMAP_SCALE, 3.8 * TILE * MINIMAP_SCALE, MINIMAP_TILE / 4, MINIMAP_TILE / 4))

    def fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, True, DARKORANGE)
        self.sc.blit(render, FPS_POS)

class Sprite(pygame.sprite.Sprite):
    def __init__(self, *group, image_path='', pos=(0, 0), player_class=player.Player((0, 0)), scale=1, v_shift=0):
        super().__init__(*group)
        self.image = pygame.image.load(os.path.join('resources/sprites/' + image_path)).convert_alpha()
        self.x, self.y = pos
        self.player = player_class
        self.scale = scale
        self.v_shift = v_shift

    def locate(self, walls):
        dx, dy = self.x - self.player.x, self.y - self.player.y
        obj_angle = (180 - degrees(atan2(dy, dx))) % 360
        angle_between = (obj_angle - (360 - self.player.angle)) % 360
        if 180 - HALF_FOV - ADDITIONAL_ANGLE <= angle_between <= 180 + HALF_FOV + ADDITIONAL_ANGLE:
            cur_ray = NUM_RAYS - ((angle_between - 180 + HALF_FOV) // DELTA_ANGLE + 1)
            depth = abs((dx / cos(radians(obj_angle))) * cos(radians(HALF_FOV - cur_ray * DELTA_ANGLE)))
            proj_height = min(PROJECTION_COEFF / depth * self.scale, HEIGHT * 2)
            pos = (cur_ray * SCALE,
                   HALF_HEIGHT - proj_height / 2 + self.v_shift * proj_height / 2)
            sprite = pygame.transform.scale(self.image, (proj_height, proj_height))
            return depth, sprite, pos
        return [False]
