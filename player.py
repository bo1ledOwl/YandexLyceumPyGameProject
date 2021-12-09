from settings import *
import pygame
import math

class Player:
    def __init__(self):
        self.x, self.y = PLAYER_START_POS
        self.angle = PLAYER_ANGLE

    def movement(self):
        sin_a = math.sin(math.radians(self.angle))
        cos_a = math.cos(math.radians(self.angle))
        keys = pygame.key.get_pressed()
        # ниже страшная вещь для перемещения как в шутерах
        if keys[pygame.K_w]:
            self.x += PLAYER_SPEED * cos_a
            self.y += PLAYER_SPEED * sin_a
        if keys[pygame.K_s]:
            self.x += -PLAYER_SPEED * cos_a
            self.y += -PLAYER_SPEED * sin_a
        if keys[pygame.K_a]:
            self.x += PLAYER_SPEED * sin_a
            self.y -= PLAYER_SPEED * cos_a
        if keys[pygame.K_d]:
            self.x += -PLAYER_SPEED * sin_a
            self.y -= -PLAYER_SPEED * cos_a

    def rotate_camera(self, mouse_move=(0, 0)):
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        if mouse_move[0] < 0:
            self.angle += PLAYER_ROTATE_SPEED * mouse_move[0]
        elif mouse_move[0] > 0:
            self.angle -= PLAYER_ROTATE_SPEED * -mouse_move[0]
        pygame.mouse.set_pos([SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2])
