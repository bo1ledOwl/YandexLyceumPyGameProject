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

    def interact(self):
        sin_a = math.sin(math.radians(self.angle))
        cos_a = math.cos(math.radians(self.angle))
        coords = map_coords(self.x + TILE * cos_a, self.y + TILE * sin_a)
        door = world_map.get(coords, False)
        if door:
            world_map.pop(coords)
