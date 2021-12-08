import pygame
from settings import *
from player import Player
import math
from map import Map
from drawing import Drawer
from ray_casting import ray_casting_func

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))

# pygame.mixer.music.load('the_only_thing_they_fear_is_you.wav')
# pygame.mixer.music.play(-1)
# pygame.mixer.music.set_volume(0.3)

clock = pygame.time.Clock()
game_map = Map("maps/map.png")
drawer = Drawer(sc, game_map)
player = Player()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    sc.fill(BLACK)

    drawer.draw_player(player)
    drawer.draw_map()
    print(player.angle)
    # ray_casting_func(player, game_map, sc)
    player.movement()

    pygame.display.flip()
    # print(clock.get_fps())
    clock.tick()
