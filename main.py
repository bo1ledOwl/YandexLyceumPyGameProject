import pygame
from settings import *
from map import *
from player import Player
import math
from drawing import Drawer
from ray_casting import ray_casting_func

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()
drawer = Drawer(sc)
player = Player(PLAYER_START_POSITION)

font = pygame.font.SysFont('Arial', 36, bold=True)

paused = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if not paused:
                    paused = True
                    pygame.mouse.set_visible(True)
                    pygame.event.set_grab(False)
                else:
                    paused = False

        if event.type == pygame.MOUSEMOTION:
            if not paused:
                player.rotate_camera(event.rel)
            # print(event.rel)

    sc.fill(BLACK)
    # print(player.angle)
    drawer.draw_background()
    ray_casting_func(player, sc)
    drawer.draw_minimap(player)
    if not paused:
        player.movement()
        drawer.fps(clock)
    else:
        render = font.render("Пауза", True, WHITE)
        sc.blit(render, PAUSE_POS)

    pygame.display.flip()
    clock.tick(FPS)
