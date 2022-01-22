import math
import os
import pygame
import player
from ray_casting import ray_casting
from settings import *
from functions import *
from math import *
from map import world_map


class Drawer:
    def __init__(self, surface):
        self.sc = surface
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        folder = os.path.abspath(__file__).replace('drawing.py', '') + 'resources/walls'
        files = os.listdir(folder)
        self.textures = {}
        for i in range(len(files)):
            self.textures[i] = pygame.image.load(folder + '/' + files[i]).convert()

    def background(self):
        pygame.draw.rect(self.sc, SKYBLUE, (0, 0, WIDTH, HALF_HEIGHT))
        pygame.draw.rect(self.sc, DARKGRAY, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))

    def world(self, objects, player):
        walls = ray_casting(player, self.textures)
        for obj in sorted(list(walls.values()) + list(map(lambda obj: obj.locate(), objects)), key=lambda a: a[0], reverse=True):
            if obj[0]:
                self.sc.blit(obj[1], obj[2])

    def minimap(self, player):
        pygame.draw.rect(self.sc, BLACK, (0, 0, MAP_WIDTH * MINIMAP_SCALE, MAP_HEIGHT * MINIMAP_SCALE))
        for wall in world_map:
            pygame.draw.rect(self.sc, PURPLE, (wall[0] * MINIMAP_SCALE, wall[1] * MINIMAP_SCALE,
                                               TILE * MINIMAP_SCALE, TILE * MINIMAP_SCALE))
        x, y = player.x, player.y
        pygame.draw.line(self.sc, GREEN, (x * MINIMAP_SCALE, y * MINIMAP_SCALE),
                         ((x + MINIMAP_DEPTH * cos(radians(player.angle - HALF_FOV))) * MINIMAP_SCALE,
                         (y + MINIMAP_DEPTH * sin(radians(player.angle - HALF_FOV))) * MINIMAP_SCALE))
        pygame.draw.line(self.sc, GREEN, (x * MINIMAP_SCALE, y * MINIMAP_SCALE),
                         ((x + MINIMAP_DEPTH * cos(radians(player.angle + HALF_FOV))) * MINIMAP_SCALE,
                          (y + MINIMAP_DEPTH * sin(radians(player.angle + HALF_FOV))) * MINIMAP_SCALE))
        pygame.draw.rect(self.sc, RED,
                         ((x - 15) * MINIMAP_SCALE, (y - 15) * MINIMAP_SCALE, 60 * MINIMAP_SCALE, 60 * MINIMAP_SCALE))

    def fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, True, DARKORANGE)
        self.sc.blit(render, FPS_POS)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, *group, image_path='', pos=(0, 0), static=True, side=0, player_class=player.Player((0, 0)), scale=1, v_shift=0):
        super().__init__(*group)
        self.images = {}
        folder = os.path.abspath(__file__).replace('drawing.py', '') + 'resources/sprites/' + image_path
        files = os.listdir(folder)
        for i in range(len(files)):
            self.images[i * ONE_VIEW_ANGLE] = pygame.image.load(folder + '/' + files[i]).convert_alpha()
        self.x, self.y = pos
        self.player = player_class
        self.scale = scale
        self.v_shift = v_shift
        self.side = side
        self.speed = PLAYER_SPEED / 2
        self.rotate_speed = PLAYER_ROTATE_SPEED * 5
        self.static = static
        self.angle = 0

    def move(self):
        if abs(self.x - self.player.x) > 25 and abs(self.y - self.player.y) > 25:
            dx, dy = self.player.x - self.x, self.player.y - self.y
            obj_angle = (180 - degrees(atan2(dy, dx))) % 360
            self.x, self.y = check_intersection(self.x, self.y,
                             -cos(radians(obj_angle)) * PLAYER_SPEED // 2, sin(radians(obj_angle)) * PLAYER_SPEED // 2, self.side)
        angle_between = (self.angle - (360 - self.player.angle)) % 360
        if 2 < angle_between <= 180:
            self.angle -= self.rotate_speed
        elif 180 < angle_between < 358:
            self.angle += self.rotate_speed
        self.angle %= 360

    def locate(self):
        dx, dy = self.x - self.player.x, self.y - self.player.y
        obj_angle = (180 - degrees(atan2(dy, dx))) % 360
        angle_between = (obj_angle - (360 - self.player.angle)) % 360
        if 180 - HALF_FOV - ADDITIONAL_ANGLE <= angle_between <= 180 + HALF_FOV + ADDITIONAL_ANGLE:
            cur_ray = NUM_RAYS - ((angle_between - 180 + HALF_FOV) // DELTA_ANGLE + 1)
            depth = abs((dx / cos(radians(obj_angle))) * cos(radians(HALF_FOV - cur_ray * DELTA_ANGLE)))
            proj_height = min(PROJECTION_COEFF / max(depth, 0.0000001) * self.scale, HEIGHT * 2)
            pos = (cur_ray * SCALE,
                   HALF_HEIGHT - proj_height / 2 + self.v_shift * proj_height / 2)
            if not self.static:
                sprite = pygame.transform.scale(self.images[(((360 - self.player.angle) - self.angle)
                    % 360 + ONE_VIEW_ANGLE / 2) % 360 // ONE_VIEW_ANGLE * ONE_VIEW_ANGLE], (proj_height, proj_height))
            else:
                sprite = pygame.transform.scale(self.images[0], (proj_height, proj_height))
            return depth, sprite, pos
        return [False]
