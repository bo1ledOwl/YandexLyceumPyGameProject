import pygame
import math
import sys
from settings import *
from map import *
from player import Player, Weapon
from drawing import *


def terminate():
    pygame.quit()
    sys.exit()


pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()
drawer = Drawer(sc)
player = Player(PLAYER_START_POSITION)
weapon = Weapon('Shotgun', 15)

enemies = [Soldier1, Soldier2, Imp, Cacodemon]  # связь цветов на карте с классами объектов
objects = [Barrel, Pedestal]

# подготовка объектов на карте
game_objects = []
for obj in enemies_coords:
    game_objects.append(enemies[enemies_coords[obj]](player, obj))
for obj in objects_coords:
    game_objects.append(objects[objects_coords[obj]](player, obj))

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
                        player.shoot(game_objects, drawer.walls, weapon)

    sc.fill(BLACK)
    drawer.background()
    drawer.world(game_objects, player)
    weapon.draw(sc)
    drawer.minimap(player)
    if not paused:
        player.movement()
        weapon.animation_frame()
        for obj in game_objects:
            if not obj.static:
                if obj.alive:
                    obj.interact()
        drawer.fps(clock)
    else:
        render = font.render("Пауза", True, WHITE)
        sc.blit(render, PAUSE_POS)

    pygame.display.flip()
    clock.tick(FPS)
