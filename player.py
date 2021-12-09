from settings import *
from map import *
import pygame
import math

class Player:
    def __init__(self, start_coords):
        self.x, self.y = start_coords
        self.angle = PLAYER_ANGLE

    def check_intersection(self):
        # проверка на вход в стену
        if map_coords(self.x, self.y) in world_map:
            return True
        # далее лучом назван центральный луч игрока (зелёный на миникарте)
        # иначе движемся по доступной оси
        # проверка если луч смотрит вверх
        if 180 < self.angle < 360:
            # проверка на вхождение по иксу
            if map_coords(self.x + 1, self.y) in world_map or map_coords(self.x - 1, self.y) in world_map:
                self.y += PLAYER_SPEED * self.sin_a
            # на вхождение по игреку
            elif map_coords(self.x, self.y + 1) in world_map or map_coords(self.x, self.y + 1) in world_map:
                if 270 < self.angle < 360:
                    self.x += PLAYER_SPEED
                else:
                    self.x -= PLAYER_SPEED
            return False
        # аналогично если луч смотрит вниз
        if map_coords(self.x + 1, self.y) in world_map or map_coords(self.x - 1, self.y) in world_map:
            self.y -= PLAYER_SPEED * self.sin_a
        elif map_coords(self.x, self.y + 1) in world_map or map_coords(self.x, self.y + 1) in world_map:
            if 90 < self.angle < 180:
                self.x -= PLAYER_SPEED
            else:
                self.x += PLAYER_SPEED
        return False


    def movement(self):
        self.sin_a = math.sin(math.radians(self.angle))
        self.cos_a = math.cos(math.radians(self.angle))
        keys = pygame.key.get_pressed()
        # ниже страшная вещь для перемещения как в шутерах
        save_x = self.x
        save_y = self.y
        if keys[pygame.K_w]:
            self.x += PLAYER_SPEED * self.cos_a
            if self.check_intersection():
                self.x = save_x
            self.y += PLAYER_SPEED * self.sin_a
            if self.check_intersection():
                self.y = save_y
        if keys[pygame.K_s]:
            self.x += -PLAYER_SPEED * self.cos_a
            if self.check_intersection():
                self.x = save_x
            self.y += -PLAYER_SPEED * self.sin_a
            if self.check_intersection():
                self.y = save_y
        if keys[pygame.K_a]:
            self.x += PLAYER_SPEED * self.sin_a
            if self.check_intersection():
                self.x = save_x
            self.y -= PLAYER_SPEED * self.cos_a
            if self.check_intersection():
                self.y = save_y
        if keys[pygame.K_d]:
            self.x += -PLAYER_SPEED * self.sin_a
            if self.check_intersection():
                self.x = save_x
            self.y -= -PLAYER_SPEED * self.cos_a
            if self.check_intersection():
                self.y = save_y

    def rotate_camera(self, mouse_move=(0, 0)):
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        if mouse_move[0] < 0:
            self.angle += PLAYER_ROTATE_SPEED * mouse_move[0]
        elif mouse_move[0] > 0:
            self.angle += PLAYER_ROTATE_SPEED * mouse_move[0]
        self.angle = self.angle % 360
        pygame.mouse.set_pos([WIDTH // 2, HEIGHT // 2])
