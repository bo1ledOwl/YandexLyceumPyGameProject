import math
import os
import pygame
import player
from ray_casting import ray_casting
from settings import *
from functions import *
from math import *
from map import world_map


class Drawer:  # класс для отрисовки карты и интерфейса
    def __init__(self, surface):
        self.sc = surface
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        folder = os.path.abspath(__file__).replace('drawing.py', '') + 'resources/walls'
        files = os.listdir(folder)
        self.textures = {}
        # текстуры стен
        for i in range(len(files)):
            self.textures[files[i][:files[i].find('.')]] = pygame.image.load(folder + '/' + files[i]).convert()

    def background(self):
        pygame.draw.rect(self.sc, SKYBLUE, (0, 0, WIDTH, HALF_HEIGHT))
        pygame.draw.rect(self.sc, DARKGRAY, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))

    def world(self, objects, player):
        self.walls = ray_casting(player, self.textures)
        for obj in sorted(list(self.walls.values()) + list(map(lambda obj: obj.locate(), objects)),  # список для отрисовки объектов
                          key=lambda a: a[0], reverse=True):
            if obj[0]:  # проверка на видимость объекта
                self.sc.blit(obj[1], obj[2])

    def minimap(self, player):
        # фон миникарты
        pygame.draw.rect(self.sc, BLACK, (0, 0, MAP_WIDTH * MINIMAP_SCALE, MAP_HEIGHT * MINIMAP_SCALE))
        # стены на миникарте
        for wall in world_map:
            if world_map[wall][0] != 'd':
                pygame.draw.rect(self.sc, PURPLE, (wall[0] * MINIMAP_SCALE, wall[1] * MINIMAP_SCALE,
                                                   TILE * MINIMAP_SCALE, TILE * MINIMAP_SCALE))
        x, y = player.x, player.y
        # линии границ поля видимости игрока
        pygame.draw.line(self.sc, GREEN, (x * MINIMAP_SCALE, y * MINIMAP_SCALE),
                         ((x + MINIMAP_DEPTH * cos(radians(player.angle - HALF_FOV))) * MINIMAP_SCALE,
                          (y + MINIMAP_DEPTH * sin(radians(player.angle - HALF_FOV))) * MINIMAP_SCALE))
        pygame.draw.line(self.sc, GREEN, (x * MINIMAP_SCALE, y * MINIMAP_SCALE),
                         ((x + MINIMAP_DEPTH * cos(radians(player.angle + HALF_FOV))) * MINIMAP_SCALE,
                          (y + MINIMAP_DEPTH * sin(radians(player.angle + HALF_FOV))) * MINIMAP_SCALE))
        # сам игрок на миникарте
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
        # все 8 возможных положений объекта если таковые есть
        for i in range(len(files)):
            self.images[i * ONE_VIEW_ANGLE] = pygame.image.load(folder + '/' + files[i]).convert_alpha()
        self.x, self.y = pos
        self.player = player_class
        self.scale = scale
        self.v_shift = v_shift
        self.side = side
        self.static = static
        self.angle = 0

    @property
    def dist(self):
        return sqrt((self.x - self.player.x) ** 2 + (self.y - self.player.y) ** 2)

    @property
    def cur_ray(self):
        # находится ли объект в поле зрения игрока, и если да, на каком луче
        dx, dy = self.x - self.player.x, self.y - self.player.y
        obj_angle = (180 - degrees(atan2(dy, dx))) % 360
        angle_between = (obj_angle - (360 - self.player.angle)) % 360
        if 180 - HALF_FOV <= angle_between <= 180 + HALF_FOV:
            return NUM_RAYS - ((angle_between - 180 + HALF_FOV) // DELTA_ANGLE + 1)
        return False

    def locate(self):
        # подготовка спрайта к отрисовке
        dx, dy = self.x - self.player.x, self.y - self.player.y
        obj_angle = (180 - degrees(atan2(dy, dx))) % 360
        angle_between = (obj_angle - (360 - self.player.angle)) % 360  # угол между игроком и спрайтом
        if 180 - HALF_FOV - ADDITIONAL_ANGLE <= angle_between <= 180 + HALF_FOV + ADDITIONAL_ANGLE:  # проверка на видимость
            cur_ray = NUM_RAYS - ((angle_between - 180 + HALF_FOV) // DELTA_ANGLE + 1)
            depth = self.dist * cos(radians(HALF_FOV - cur_ray * DELTA_ANGLE))
            proj_height = min(PROJECTION_COEFF / max(depth, 0.0000001) * self.scale, HEIGHT * 2)  # размеры объекта
            # позиция на экране
            pos = (cur_ray * SCALE,
                   HALF_HEIGHT - proj_height / 2 + self.v_shift * proj_height / 2)
            return self.draw(True, proj_height, depth, pos)
        return self.draw(False)

    def draw(self, visible, proj_height=0, depth=0, pos=(0, 0)):
        # метод для отрисовки, выполняется только если объект в поле видимости, изменен у класса врагов
        if visible:
            sprite = pygame.transform.scale(self.images[0], (proj_height, proj_height))
            return depth, sprite, pos
        return [False]


class Enemy(Sprite):
    def __init__(self, image, player, pos, speed, side, scale, v_shift, hp, attack_cooldown):
        super().__init__(image_path=image, pos=pos, static=False, side=side, player_class=player, scale=scale,
                         v_shift=v_shift)
        # текущее состояние
        self.attacking = False
        self.alive = True
        # параметры
        self.hp = hp
        self.death_animation = []
        self.attack_animation = []
        self.attack_cooldown = 0  # время отката атаки
        self.attack_cooldown_max = attack_cooldown
        self.speed = speed
        self.rotate_speed = PLAYER_ROTATE_SPEED * 6
        self.pain_sound = pygame.mixer.Sound(f'resources/sound/pain.wav')
        self.death_sound = pygame.mixer.Sound(f'resources/sound/death.wav')
        self.cur_frame = 0
        folder = os.path.abspath(__file__).replace('drawing.py',
                                                   '') + 'resources/sprites/' + self.image_path + '/death/'
        files = os.listdir(folder)
        for i in range(len(files)):
            self.death_animation.append(pygame.image.load(folder + '/' + files[i]).convert_alpha())
        folder = os.path.abspath(__file__).replace('drawing.py',
                                                   '') + 'resources/sprites/' + self.image_path + '/attack/'
        files = os.listdir(folder)
        for i in range(len(files)):
            self.attack_animation.append(pygame.image.load(folder + '/' + files[i]).convert_alpha())

    def interact(self):
        if abs(self.x - self.player.x) > WALL_SAFE_RANGE or abs(self.y - self.player.y) > WALL_SAFE_RANGE:  # перемещение к игроку
            dx, dy = self.player.x - self.x, self.player.y - self.y
            obj_angle = (180 - degrees(atan2(dy, dx))) % 360
            self.x, self.y = check_intersection(self.x, self.y,
                                                -cos(radians(obj_angle)) * self.speed,
                                                sin(radians(obj_angle)) * self.speed, self.side)
        angle_between = (self.angle - (360 - self.player.angle)) % 360
        # атака
        if not self.attacking and self.attack_cooldown > 0:
            self.attack_cooldown += 1
            self.attack_cooldown %= self.attack_cooldown_max
        if self.attack_cooldown == 0:
            self.attacking = True
        # поворот объекта
        if 2 < angle_between <= 180:
            self.angle -= self.rotate_speed
        elif 180 < angle_between < 358:
            self.angle += self.rotate_speed
        self.angle %= 360

    def draw(self, visible, proj_height=0, depth=0, pos=(0, 0)):
        if visible:
            if self.alive:
                if self.attacking:
                    # анимация атаки
                    sprite = pygame.transform.scale(self.attack_animation[int(self.cur_frame)], (proj_height, proj_height))
                    if self.cur_frame < len(self.attack_animation) - 1:
                        self.cur_frame += 0.15 * (60 / FPS)
                    if int(self.cur_frame) == len(self.attack_animation) - 1:
                        self.cur_frame = 0
                        self.attacking = False
                        self.attack_cooldown = 1
                else:
                    # статичное изображение врага
                    sprite = pygame.transform.scale(self.images[(((360 - self.player.angle) - self.angle)
                                                                 % 360 + ONE_VIEW_ANGLE / 2) % 360 // ONE_VIEW_ANGLE * ONE_VIEW_ANGLE],
                                                    (proj_height, proj_height))
            else:
                # анимация смерти
                sprite = pygame.transform.scale(self.death_animation[int(self.cur_frame)], (proj_height, proj_height))
                if self.cur_frame < len(self.death_animation) - 1:
                    self.cur_frame += 0.2 * (60 / FPS)
            return depth, sprite, pos
        return [False]

    def death(self):
        if self.attacking:
            self.cur_frame = 0
        if self.alive:
            self.alive = False
            self.death_sound.play()

    def hurt(self):
        self.pain_sound.play()

# готовые классы врагов
class Cacodemon(Enemy):
    def __init__(self, player, pos):
        super().__init__(image='Cacodemon', player=player, pos=pos, speed=PLAYER_SPEED // 2, side=50,
                         scale=1, v_shift=0, hp=40, attack_cooldown=60)


class Imp(Enemy):
    def __init__(self, player, pos):
        super().__init__(image='Imp', player=player, speed=PLAYER_SPEED / 3, pos=pos, side=25,
                         scale=0.5, v_shift=0.75, hp=15, attack_cooldown=50)


class Soldier1(Enemy):
    def __init__(self, player, pos):
        super().__init__(image='Soldier1', player=player, speed=PLAYER_SPEED / 3, pos=pos, side=25,
                         scale=0.5, v_shift=0.75, hp=15, attack_cooldown=65)


class Soldier2(Enemy):
    def __init__(self, player, pos):
        super().__init__(image='Soldier2', player=player, speed=PLAYER_SPEED / 3, pos=pos, side=25,
                         scale=0.5, v_shift=0.75, hp=15, attack_cooldown=65)


class Barrel(Sprite):
    def __init__(self, player, pos):
        super().__init__(image_path='Barrel', pos=pos, player_class=player, scale=0.5, v_shift=1.5)


class Pedestal(Sprite):
    def __init__(self, player, pos):
        super().__init__(image_path='Pedestal', pos=pos, player_class=player, scale=0.5, v_shift=1.5)
