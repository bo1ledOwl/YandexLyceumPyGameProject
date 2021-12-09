import pygame
from settings import *
from player import Player
import math
from drawing import Drawer
from ray_casting import ray_casting_func

pygame.init()
sc = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()
drawer = Drawer(sc)
player = Player()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit()
    sc.fill(BLACK)

    # drawer.draw_player(player)
    # print(player.angle)
    drawer.draw_background()
    ray_casting_func(player, sc)
    drawer.draw_minimap(player)
    player.movement()

    pygame.display.flip()
    #print(int(clock.get_fps()))
    clock.tick(FPS)
