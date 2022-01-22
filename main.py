import pygame
import math
import sys
from settings import *
from map import *
from player import Player
from drawing import Drawer, Sprite

def terminate():
	pygame.quit()
	sys.exit()

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()
drawer = Drawer(sc)
player = Player(PLAYER_START_POSITION)

objects = [Sprite(image_path='Cacodemon', pos=(17 * TILE, 13 * TILE), static=False, side=50, player_class=player, scale=1, v_shift = 0),
           Sprite(image_path='Barrel', pos=(17 * TILE, 13 * TILE), player_class=player, scale=0.5, v_shift = 1.5),
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

    sc.fill(BLACK)
    drawer.background()
    drawer.world(objects, player)
    drawer.minimap(player)
    if not paused:
        player.movement()
        for obj in objects:
            if not obj.static:
                obj.move()
        drawer.fps(clock)
    else:
        render = font.render("Пауза", True, WHITE)
        sc.blit(render, PAUSE_POS)

    pygame.display.flip()
    clock.tick(FPS)
