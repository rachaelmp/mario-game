WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BRIGHTPURPLE = (255, 0, 255)
LIGHTBLUE = (0, 155, 155)

TITLE = 'Super Mario Bros.'

SCALE = 2
FPS = 60

WIDTH = 256 * SCALE
HEIGHT = 240 * SCALE

BG_COLOR = LIGHTBLUE
FONT = 'arial'
SPRITESHEET = "allsprites.png"

PLAYER_ACCELERATION = 0.4
PLAYER_FRICTION = -0.1
PLAYER_GRAV = 0.8
PLAYER_JUMP = 12

LIVES_DEFAULT = 3
TIME_LIMIT = 400

# Starting platforms and blocks
PLATFORM_LIST = []
BLOCK_LIST = []

# GROUND
for x in range(0, 15 * 69 * SCALE, 15 * SCALE):
    PLATFORM_LIST.append((x, HEIGHT - 15 * SCALE // 2, 0))
    PLATFORM_LIST.append((x, HEIGHT - 15 * SCALE // 2 - 15 * SCALE, 0))
    PLATFORM_LIST.append((x, HEIGHT - 15 * SCALE // 2 - 30 * SCALE, 0))

for x in range(15 * 71 * SCALE, 15 * 86 * SCALE, 15 * SCALE):
    PLATFORM_LIST.append((x, HEIGHT - 15 * SCALE // 2, 0))
    PLATFORM_LIST.append((x, HEIGHT - 15 * SCALE // 2 - 15 * SCALE, 0))
    PLATFORM_LIST.append((x, HEIGHT - 15 * SCALE // 2 - 30 * SCALE, 0))

for x in range(15 * 89 * SCALE, 15 * 153 * SCALE, 15 * SCALE):
    PLATFORM_LIST.append((x, HEIGHT - 15 * SCALE // 2, 0))
    PLATFORM_LIST.append((x, HEIGHT - 15 * SCALE // 2 - 15 * SCALE, 0))
    PLATFORM_LIST.append((x, HEIGHT - 15 * SCALE // 2 - 30 * SCALE, 0))

for x in range(15 * 155 * SCALE, 15 * 208 * SCALE, 15 * SCALE):
    PLATFORM_LIST.append((x, HEIGHT - 15 * SCALE // 2, 0))
    PLATFORM_LIST.append((x, HEIGHT - 15 * SCALE // 2 - 15 * SCALE, 0))
    PLATFORM_LIST.append((x, HEIGHT - 15 * SCALE // 2 - 30 * SCALE, 0))

# PIPES
PLATFORM_LIST.append((15 * 28 * SCALE, HEIGHT - 18 * SCALE // 2 - 60 * SCALE, 2))

PLATFORM_LIST.append((15 * 38 * SCALE, HEIGHT - 18 * SCALE // 2 - 75 * SCALE - 15 * SCALE, 2))
PLATFORM_LIST.append((15 * 38 * SCALE, HEIGHT - 18 * SCALE // 2 - 60 * SCALE + 15 * SCALE, 3))
PLATFORM_LIST.append((15 * 38 * SCALE, HEIGHT - 18 * SCALE // 2 - 75 * SCALE + 15 * SCALE, 3))

PLATFORM_LIST.append((15 * 48 * SCALE, HEIGHT - 18 * SCALE // 2 - 90 * SCALE - 15 * SCALE, 2))
PLATFORM_LIST.append((15 * 48 * SCALE, HEIGHT - 18 * SCALE // 2 - 60 * SCALE + 15 * SCALE, 3))
PLATFORM_LIST.append((15 * 48 * SCALE, HEIGHT - 18 * SCALE // 2 - 75 * SCALE + 15 * SCALE, 3))
PLATFORM_LIST.append((15 * 48 * SCALE, HEIGHT - 18 * SCALE // 2 - 90 * SCALE + 15 * SCALE, 3))

PLATFORM_LIST.append((15 * 58 * SCALE, HEIGHT - 18 * SCALE // 2 - 100 * SCALE - 15 * SCALE, 2))
PLATFORM_LIST.append((15 * 58 * SCALE, HEIGHT - 18 * SCALE // 2 - 60 * SCALE + 15 * SCALE, 3))
PLATFORM_LIST.append((15 * 58 * SCALE, HEIGHT - 18 * SCALE // 2 - 75 * SCALE + 15 * SCALE, 3))
PLATFORM_LIST.append((15 * 58 * SCALE, HEIGHT - 18 * SCALE // 2 - 90 * SCALE + 15 * SCALE, 3))
PLATFORM_LIST.append((15 * 58 * SCALE, HEIGHT - 18 * SCALE // 2 - 100 * SCALE + 15 * SCALE, 3))

# STEPS
for y in range(1, 5):
    for x in range(15 * 155 * SCALE, 15 * (160 - y) * SCALE, 15 * SCALE):
        PLATFORM_LIST.append((x, HEIGHT - 15 * SCALE // 2 - (2 + y) * 15 * SCALE, 1))

for y in range(1, 5):
    for x in range(15 * 140 * SCALE, 15 * (145 - y) * SCALE, 15 * SCALE):
        PLATFORM_LIST.append((x, HEIGHT - 15 * SCALE // 2 - (2 + y) * 15 * SCALE, 1))

for y in range(1, 5):
    for x in range(15 * (133 + y) * SCALE, 15 * 138 * SCALE, 15 * SCALE):
        PLATFORM_LIST.append((x, HEIGHT - 15 * SCALE // 2 - (2 + y) * 15 * SCALE, 1))

PLATFORM_LIST.append((15 * 18 * SCALE, HEIGHT - 90 * SCALE // 2 - 60 * SCALE, 4))
PLATFORM_LIST.append((15 * 23 * SCALE, HEIGHT - 120 * SCALE // 2 - 90 * SCALE, 4))

for x in range(15 * 21 * SCALE, 15 * 26 * SCALE, 15 * SCALE):
    PLATFORM_LIST.append((x, HEIGHT - 90 * SCALE // 2 - 60 * SCALE, 4))


