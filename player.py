from settings import *
from map import *
from functions import *
import pygame
import math


class Player:
    def __init__(self, start_coords):
        self.x, self.y = start_coords
        self.angle = PLAYER_ANGLE

    def keyboard(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.interact()

    def movement(self):
        sin_a = math.sin(math.radians(self.angle))
        cos_a = math.cos(math.radians(self.angle))
        keys = pygame.key.get_pressed()
        # реакция на кнопки с проверкой на столкновения со стенами
        if keys[pygame.K_w]:
            delta_x = PLAYER_SPEED * cos_a
            delta_y = PLAYER_SPEED * sin_a
            self.x, self.y = check_intersection(self.x, self.y, delta_x, delta_y)
        if keys[pygame.K_s]:
            delta_x = -PLAYER_SPEED * cos_a
            delta_y = -PLAYER_SPEED * sin_a
            self.x, self.y = check_intersection(self.x, self.y, delta_x, delta_y)
        if keys[pygame.K_a]:
            delta_x = PLAYER_SPEED * sin_a
            delta_y = -PLAYER_SPEED * cos_a
            self.x, self.y = check_intersection(self.x, self.y, delta_x, delta_y)
        if keys[pygame.K_d]:
            delta_x = -PLAYER_SPEED * sin_a
            delta_y = PLAYER_SPEED * cos_a
            self.x, self.y = check_intersection(self.x, self.y, delta_x, delta_y)

    def rotate_camera(self, mouse_move=(0, 0)):
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        if mouse_move[0]:
            self.angle += PLAYER_ROTATE_SPEED * mouse_move[0]
            self.angle %= 360
        pygame.mouse.set_pos([WIDTH // 2, HEIGHT // 2])

    def shoot(self, objects, walls, weapon):
        weapon.in_animation = True
        weapon.sound.play()
        sin_a = math.sin(math.radians(self.angle))
        cos_a = math.cos(math.radians(self.angle))
        coords = map_coords(self.x + TILE * cos_a, self.y + TILE * sin_a)
        # сортировка объектов по расстоянию
        objects_by_dist = list(filter(lambda obj: not obj.static and obj.alive, sorted(objects, key=lambda a: a.dist)))
        for obj in objects_by_dist:
            if obj.dist < walls.get(int(obj.cur_ray), [False])[0] and obj.cur_ray:
                # нанесение урона
                if obj.hp > 0:
                    obj.hp -= weapon.damage
                    obj.hurt()
                # убийство врага
                if obj.hp <= 0:
                    obj.death()
                break

    def interact(self):
        # взаимодействие с дверьми
        sin_a = math.sin(math.radians(self.angle))
        cos_a = math.cos(math.radians(self.angle))
        coords = map_coords(self.x + TILE * cos_a, self.y + TILE * sin_a)
        if world_map.get(coords, False):
            world_map.pop(coords)


class Weapon(pygame.sprite.Sprite):
    def __init__(self, name, damage):
        super().__init__()
        self.name = name
        self.damage = damage
        self.sound = pygame.mixer.Sound(f'resources/sound/{name.lower()}.wav')
        self.animation = {}
        self.in_animation = False
        self.cur_frame = 0
        folder = os.path.abspath(__file__).replace('player.py', '') + 'resources/sprites/weapon/' + name
        files = os.listdir(folder)
        for i in range(len(files)):
            self.animation[i] = pygame.image.load(folder + '/' + files[i]).convert_alpha()

    def animation_frame(self):
        # анимация выстрела
        if self.in_animation and self.cur_frame < len(self.animation) - 9:
            self.cur_frame += 0.25 * (60 / FPS)
        else:
            self.cur_frame = 0
            self.in_animation = False

    def draw(self, sc):
        sc.blit(self.animation[int(self.cur_frame)], (HALF_WIDTH * 0.65, HALF_HEIGHT * 1.25))
