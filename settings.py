import math


def map_coords(x, y):
    return int((x // TILE) * TILE), int((y // TILE) * TILE)


# основные настройки
WIDTH = 1280
HEIGHT = 720
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 60
TILE = 100
MINIMAP_SCALE = 0.1
MINIMAP_TILE = TILE * MINIMAP_SCALE
MINIMAP_DEPTH = 1000 * MINIMAP_SCALE
FPS_POS = (WIDTH - 65, 5)
PAUSE_POS = (HALF_WIDTH - 50, 100)

# настройки ray casting
FOV = 60
HALF_FOV = FOV / 2
NUM_RAYS = 320
DELTA_ANGLE = FOV / NUM_RAYS
DIST = NUM_RAYS / math.tan(math.radians(HALF_FOV))
PROJECTION_COEFF = 1.5 * DIST * TILE
SCALE = WIDTH / NUM_RAYS
CENTRAL_RAY = NUM_RAYS // 2 - 1

# настройки текстур
TEXTURE_WIDTH = 1200
TEXTURE_HEIGHT = 1200
HALF_TEXTURE_HEIGHT = TEXTURE_HEIGHT // 2
TEXTURE_SCALE = TEXTURE_WIDTH // TILE

# настройки спрайтов
ADDITIONAL_RAYS = 75
ADDITIONAL_ANGLE = DELTA_ANGLE * ADDITIONAL_RAYS

# настройки игрока
PLAYER_ANGLE = 0
PLAYER_SPEED = 5 * (60 / FPS)
PLAYER_ROTATE_SPEED = 1 * (60 / FPS) / 5
WALL_SAFE_RANGE = 30
HALF_WALL_SAFE_RANGE = WALL_SAFE_RANGE // 2

# цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
DARKGRAY = (40, 40, 40)
PURPLE = (120, 0, 120)
SKYBLUE = (0, 185, 255)
YELLOW = (220, 220, 0)
SANDY = (245, 165, 95)
DARKBROWN = (95, 60, 25)
DARKORANGE = (255, 140, 0)
