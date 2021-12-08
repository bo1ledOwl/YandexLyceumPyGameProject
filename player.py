from settings import *
import pygame
import math

class Player:
    def __init__(self):
        self.x, self.y = PLAYER_START_POS
        self.angle = PLAYER_ANGLE

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.x += PLAYER_SPEED * cos_a
            self.y += PLAYER_SPEED * sin_a
        if keys[pygame.K_s]:
            self.x += -PLAYER_SPEED * cos_a
            self.y += -PLAYER_SPEED * sin_a
        if keys[pygame.K_a]:
            self.x += PLAYER_SPEED * sin_a
            self.y += -PLAYER_SPEED * cos_a
        if keys[pygame.K_d]:
            self.x += -PLAYER_SPEED * sin_a
            self.y += PLAYER_SPEED * cos_a
        if keys[pygame.K_LEFT]:
            self.angle = (self.angle + PLAYER_ROTATE_SPEED) % 360
        if keys[pygame.K_RIGHT]:
            self.angle = (self.angle - PLAYER_ROTATE_SPEED) % 360
