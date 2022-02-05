import pygame
import math
import sys
from settings import *
from map import *
from player import Player
from drawing import *


def terminate():
    pygame.quit()
    sys.exit()


pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()
drawer = Drawer(sc)
player = Player(PLAYER_START_POSITION)
weapon = Weapon('Shotgun')

objects = [Cacodemon(player, (17 * TILE, 13 * TILE)),
           Sprite(image_path='Barrel', pos=(17 * TILE, 13 * TILE), player_class=player, scale=0.5, v_shift=1.5),
           ]

font = pygame.font.SysFont('Arial', 36, bold=True)
paused = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.KEYDOWN:
            player.keyboard()
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

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                if not paused:
                    if not weapon.in_animation:
                        player.shoot(objects, drawer.walls, weapon)

    sc.fill(BLACK)
    drawer.background()
    drawer.world(objects, player)
    weapon.draw(sc)
    drawer.minimap(player)
    if not paused:
        player.movement()
        weapon.animation_frame()
        for obj in objects:
            if not obj.static:
                if obj.hp > 0:
                    obj.move()
        drawer.fps(clock)
    else:
        render = font.render("Пауза", True, WHITE)
        sc.blit(render, PAUSE_POS)

    pygame.display.flip()
    clock.tick(FPS)
