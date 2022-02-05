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
            self.textures[files[i][:files[i].find('.')]] = pygame.image.load(folder + '/' + files[i]).convert()

    def background(self):
        pygame.draw.rect(self.sc, SKYBLUE, (0, 0, WIDTH, HALF_HEIGHT))
        pygame.draw.rect(self.sc, DARKGRAY, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))

    def world(self, objects, player):
        self.walls = ray_casting(player, self.textures)
        for obj in sorted(list(self.walls.values()) + list(map(lambda obj: obj.locate(), objects)),
                          key=lambda a: a[0], reverse=True):
            if obj[0]:
                self.sc.blit(obj[1], obj[2])

    def minimap(self, player):
        pygame.draw.rect(self.sc, BLACK, (0, 0, MAP_WIDTH * MINIMAP_SCALE, MAP_HEIGHT * MINIMAP_SCALE))
        for wall in world_map:
            if world_map[wall][0] != 'd':
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
    def __init__(self, image_path='', pos=(0, 0), static=True, side=0,
                 player_class=player.Player((0, 0)), scale=1, v_shift=0):
        super().__init__()
        self.image_path = image_path
        self.images = {}
        folder = os.path.abspath(__file__).replace('drawing.py', '') + 'resources/sprites/' + image_path + '/main/'
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

    @property
    def dist(self):
        return sqrt((self.x - self.player.x) ** 2 + (self.y - self.player.y) ** 2)

    @property
    def cur_ray(self):
        dx, dy = self.x - self.player.x, self.y - self.player.y
        obj_angle = (180 - degrees(atan2(dy, dx))) % 360
        angle_between = (obj_angle - (360 - self.player.angle)) % 360
        if 180 - HALF_FOV <= angle_between <= 180 + HALF_FOV:
            return NUM_RAYS - ((angle_between - 180 + HALF_FOV) // DELTA_ANGLE + 1)
        return False

    def locate(self):
        dx, dy = self.x - self.player.x, self.y - self.player.y
        obj_angle = (180 - degrees(atan2(dy, dx))) % 360
        angle_between = (obj_angle - (360 - self.player.angle)) % 360
        if 180 - HALF_FOV - ADDITIONAL_ANGLE <= angle_between <= 180 + HALF_FOV + ADDITIONAL_ANGLE:
            cur_ray = NUM_RAYS - ((angle_between - 180 + HALF_FOV) // DELTA_ANGLE + 1)
            depth = self.dist * cos(radians(HALF_FOV - cur_ray * DELTA_ANGLE))
            proj_height = min(PROJECTION_COEFF / max(depth, 0.0000001) * self.scale, HEIGHT * 2)
            pos = (cur_ray * SCALE,
                   HALF_HEIGHT - proj_height / 2 + self.v_shift * proj_height / 2)
            return self.draw(True, proj_height, depth, pos)
        return self.draw(False)

    def draw(self, visible, proj_height=0, depth=0, pos=(0, 0)):
        if visible:
            sprite = pygame.transform.scale(self.images[0], (proj_height, proj_height))
            return depth, sprite, pos
        return [False]


class Demon(Sprite):
    def __init__(self, image, player, pos, side, scale, v_shift, hp):
        super().__init__(image_path=image, pos=pos, static=False, side=side, player_class=player, scale=scale,
                         v_shift=v_shift)
        self.hp = hp
        self.death_animation = []
        self.cur_frame = 0
        self.alive = True
        folder = os.path.abspath(__file__).replace('drawing.py',
                                                   '') + 'resources/sprites/' + self.image_path + '/death/'
        files = os.listdir(folder)
        for i in range(len(files)):
            self.death_animation.append(pygame.image.load(folder + '/' + files[i]).convert_alpha())

    def move(self):
        if abs(self.x - self.player.x) > 25 and abs(self.y - self.player.y) > 25:
            dx, dy = self.player.x - self.x, self.player.y - self.y
            obj_angle = (180 - degrees(atan2(dy, dx))) % 360
            self.x, self.y = check_intersection(self.x, self.y,
                                                -cos(radians(obj_angle)) * PLAYER_SPEED // 2,
                                                sin(radians(obj_angle)) * PLAYER_SPEED // 2, self.side)
        angle_between = (self.angle - (360 - self.player.angle)) % 360
        if 2 < angle_between <= 180:
            self.angle -= self.rotate_speed
        elif 180 < angle_between < 358:
            self.angle += self.rotate_speed
        self.angle %= 360

    def draw(self, visible, proj_height=0, depth=0, pos=(0, 0)):
        if visible:
            if self.alive:
                sprite = pygame.transform.scale(self.images[(((360 - self.player.angle) - self.angle)
                                                % 360 + ONE_VIEW_ANGLE / 2) % 360 // ONE_VIEW_ANGLE * ONE_VIEW_ANGLE],
                                                (proj_height, proj_height))
            else:
                sprite = pygame.transform.scale(self.death_animation[int(self.cur_frame)], (proj_height, proj_height))
                if self.cur_frame < len(self.death_animation) - 1:
                    self.cur_frame += 0.2
            return depth, sprite, pos
        return [False]

    def death(self):
        if self.alive:
            self.alive = False


class Cacodemon(Demon):
    def __init__(self, player, pos):
        super().__init__(image='Cacodemon', player=player, pos=pos, side=50, scale=1, v_shift=0, hp=40)


class Weapon(pygame.sprite.Sprite):
    def __init__(self, image_path=''):
        super().__init__()
        self.image_path = image_path
        self.animation = {}
        self.in_animation = False
        self.cur_frame = 0
        folder = os.path.abspath(__file__).replace('drawing.py', '') + 'resources/sprites/weapon/' + image_path
        files = os.listdir(folder)
        for i in range(len(files)):
            self.animation[i] = pygame.image.load(folder + '/' + files[i]).convert_alpha()

    def animation_frame(self):
        if self.in_animation and self.cur_frame < len(self.animation) - 1:
            self.cur_frame += 0.25
        else:
            self.cur_frame = 0
            self.in_animation = False

    def draw(self, sc):
        sc.blit(self.animation[int(self.cur_frame)], (HALF_WIDTH * 0.65, HALF_HEIGHT * 1.25))
