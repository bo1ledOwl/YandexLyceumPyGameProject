import pygame
import math
import sys
from settings import *
from map import *
from player import Player
from drawing import Drawer, Sprite
from ray_casting import ray_casting_func

def terminate():
	pygame.quit()
	sys.exit()

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()
drawer = Drawer(sc)
player = Player(PLAYER_START_POSITION)

objects = [Sprite(image_path='barrel.png', pos=(19 * TILE, 4 * TILE), player_class=player),
           ]

font = pygame.font.SysFont('Arial', 36, bold=True)
paused = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
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
                # print(360 - player.angle)

    sc.fill(BLACK)
    drawer.background()
    drawer.world(objects, player)
    drawer.minimap(player)
    if not paused:
        player.movement()
        objects[0].angle()
        drawer.fps(clock)
    else:
        render = font.render("Пауза", True, WHITE)
        sc.blit(render, PAUSE_POS)

    pygame.display.flip()
    clock.tick(FPS)
