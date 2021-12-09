from settings import *
from map import *
import pygame
import math

class Player:
    def __init__(self, start_coords):
        self.x, self.y = start_coords
        self.angle = PLAYER_ANGLE

    def check_intersection(self, dx, dy):
        if not map_coords(self.x + PLAYER_SPEED, self.y) in world_map and dx > 0:
            self.x += dx
        elif not map_coords(self.x - PLAYER_SPEED, self.y) in world_map and dx < 0:
            self.x += dx
        if not map_coords(self.x, self.y + PLAYER_SPEED) in world_map and dy > 0:
            self.y += dy
        elif not map_coords(self.x, self.y - PLAYER_SPEED) in world_map and dy < 0:
            self.y += dy


    def movement(self):
        self.sin_a = math.sin(math.radians(self.angle))
        self.cos_a = math.cos(math.radians(self.angle))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            delta_x = PLAYER_SPEED * self.cos_a
            delta_y = PLAYER_SPEED * self.sin_a
            self.check_intersection(delta_x, delta_y)
        if keys[pygame.K_s]:
            delta_x = -PLAYER_SPEED * self.cos_a
            delta_y = -PLAYER_SPEED * self.sin_a
            self.check_intersection(delta_x, delta_y)
        if keys[pygame.K_a]:
            delta_x = PLAYER_SPEED * self.sin_a
            delta_y = -PLAYER_SPEED * self.cos_a
            self.check_intersection(delta_x, delta_y)
        if keys[pygame.K_d]:
            delta_x = -PLAYER_SPEED * self.sin_a
            delta_y = PLAYER_SPEED * self.cos_a
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