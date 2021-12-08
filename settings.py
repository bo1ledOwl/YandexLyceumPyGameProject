import math

# основные настройки
WIDTH = 1200
HEIGHT = 800
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 60
TILE = 50

# настройки ray casting
FOV = 90
HALF_FOV = FOV / 2
NUM_RAYS = 150
MAX_DEPTH = 800
DELTA_ANGLE = FOV / NUM_RAYS

# настройки игрока
PLAYER_START_POS = (HALF_WIDTH, HALF_HEIGHT)
PLAYER_ANGLE = 0
PLAYER_SPEED = 2
PLAYER_ROTATE_SPEED = 2

# цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARKGRAY = (40, 40, 40)
PURPLE = (120, 0, 120)
SKYBLUE = (0, 186, 255)
YELLOW = (220, 220, 0)
SANDY = (244, 164, 96)