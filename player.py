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

    def check_intersection(self, dx, dy, keys_count):
        if keys_count > 1:
            keys_count -= 0.5
        if not map_coords(self.x + self.check_sign(dx) * (PLAYER_SPEED + WALL_SAFE_RANGE), self.y) in world_map and \
                map_coords(self.x, self.y + self.check_sign(dy) * (PLAYER_SPEED + WALL_SAFE_RANGE)) in world_map:
            self.x += dx / keys_count
        if not map_coords(self.x, self.y + self.check_sign(dy) * (PLAYER_SPEED + WALL_SAFE_RANGE)) in world_map and \
                map_coords(self.x + self.check_sign(dx) * (PLAYER_SPEED + WALL_SAFE_RANGE), self.y) in world_map:
            self.y += dy / keys_count
        elif not map_coords(self.x + self.check_sign(dx) * (PLAYER_SPEED + WALL_SAFE_RANGE),
                            self.y + self.check_sign(dy) * (PLAYER_SPEED + WALL_SAFE_RANGE)) in world_map:
            self.x += dx / keys_count
            self.y += dy / keys_count

    def movement(self):
        sin_a = math.sin(math.radians(self.angle))
        cos_a = math.cos(math.radians(self.angle))
        keys = pygame.key.get_pressed()
        keys_count = sum(list(map(lambda a: int(a), [keys[pygame.K_w], keys[pygame.K_s], keys[pygame.K_a], keys[pygame.K_d]])))
        if keys[pygame.K_w]:
            delta_x = PLAYER_SPEED * cos_a
            delta_y = PLAYER_SPEED * sin_a
            self.check_intersection(delta_x, delta_y, keys_count)
        if keys[pygame.K_s]:
            delta_x = -PLAYER_SPEED * cos_a
            delta_y = -PLAYER_SPEED * sin_a
            self.check_intersection(delta_x, delta_y, keys_count)
        if keys[pygame.K_a]:
            delta_x = PLAYER_SPEED * sin_a
            delta_y = -PLAYER_SPEED * cos_a
            self.check_intersection(delta_x, delta_y, keys_count)
        if keys[pygame.K_d]:
            delta_x = -PLAYER_SPEED * sin_a
            delta_y = PLAYER_SPEED * cos_a
            self.check_intersection(delta_x, delta_y, keys_count)

    def rotate_camera(self, mouse_move=(0, 0)):
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        if mouse_move[0] < 0:
            self.angle += PLAYER_ROTATE_SPEED * mouse_move[0]
        elif mouse_move[0] > 0:
            self.angle += PLAYER_ROTATE_SPEED * mouse_move[0]
        self.angle = self.angle % 360
        pygame.mouse.set_pos([WIDTH // 2, HEIGHT // 2])
