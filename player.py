from settings import *
from map import *
import pygame
import math


class Player:
    def __init__(self, start_coords):
        self.x, self.y = start_coords
        self.angle = PLAYER_ANGLE

    @staticmethod
    def check_sign(n):
        if n >= 0:
            return 1
        return -1

    def check_intersection(self, dx, dy):
        if not map_coords(self.x + self.check_sign(dx) * (PLAYER_SPEED + WALL_SAFE_RANGE), self.y) in world_map and \
                map_coords(self.x, self.y + self.check_sign(dy) * (PLAYER_SPEED + WALL_SAFE_RANGE)) in world_map:
            self.x += dx
        if not map_coords(self.x, self.y + self.check_sign(dy) * (PLAYER_SPEED + WALL_SAFE_RANGE)) in world_map and \
                map_coords(self.x + self.check_sign(dx) * (PLAYER_SPEED + WALL_SAFE_RANGE), self.y) in world_map:
            self.y += dy
        elif not map_coords(self.x + self.check_sign(dx) * (PLAYER_SPEED + WALL_SAFE_RANGE),
                            self.y + self.check_sign(dy) * (PLAYER_SPEED + WALL_SAFE_RANGE)) in world_map:
            self.x += dx
            self.y += dy

    def movement(self):
        sin_a = math.sin(math.radians(self.angle))
        cos_a = math.cos(math.radians(self.angle))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            delta_x = PLAYER_SPEED * cos_a
            delta_y = PLAYER_SPEED * sin_a
            self.check_intersection(delta_x, delta_y)
        if keys[pygame.K_s]:
            delta_x = -PLAYER_SPEED * cos_a
            delta_y = -PLAYER_SPEED * sin_a
            self.check_intersection(delta_x, delta_y)
        if keys[pygame.K_a]:
            delta_x = PLAYER_SPEED * sin_a
            delta_y = -PLAYER_SPEED * cos_a
            self.check_intersection(delta_x, delta_y)
        if keys[pygame.K_d]:
            delta_x = -PLAYER_SPEED * sin_a
            delta_y = PLAYER_SPEED * cos_a
            self.check_intersection(delta_x, delta_y)

    def rotate_camera(self, mouse_move=(0, 0)):
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        if mouse_move[0] < 0:
            self.angle += PLAYER_ROTATE_SPEED * mouse_move[0]
        elif mouse_move[0] > 0:
            self.angle += PLAYER_ROTATE_SPEED * mouse_move[0]
        self.angle = self.angle % 360
        pygame.mouse.set_pos([WIDTH // 2, HEIGHT // 2])
