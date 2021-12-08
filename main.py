import pygame
from settings import *
from player import Player
import math
from drawing import Drawer
from ray_casting import ray_casting_func

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()
drawer = Drawer(sc)
player = Player()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    sc.fill(BLACK)

    drawer.draw_player(player)
    drawer.draw_map()
    # print(player.angle)
    ray_casting_func(player, sc)
    player.movement()

    pygame.display.flip()
    print(int(clock.get_fps()))
    clock.tick(FPS)
