import pygame

# Window
WINDOW_WIDTH = 288
WINDOW_HEIGHT = 512

# !!!! Bird !!!!
GRAVITY = 0.4
JUMPING_VELOCITY = 6

BIRD_SIZE = (34, 24)

BIRD_ANIMATION_COOLDOWN = 150

MAX_BIRD_ANGLE = 25
MIN_BIRD_ANGLE = -30
BIRD_DELTA_X = 10 # Imaginary velocity to create the vector and modify the rotation speed

# Blue
BLUE_BIRD_ANIMATION = [
    pygame.image.load("assets/sprites/bird/bluebird-downflap.png"),
    pygame.image.load("assets/sprites/bird/bluebird-midflap.png"),
    pygame.image.load("assets/sprites/bird/bluebird-upflap.png")

]

# Red
RED_BIRD_ANIMATION = [
    pygame.image.load("assets/sprites/bird/redbird-downflap.png"),
    pygame.image.load("assets/sprites/bird/redbird-midflap.png"),
    pygame.image.load("assets/sprites/bird/redbird-upflap.png")

]

# Yellow
YELLOW_BIRD_ANIMATION = [
    pygame.image.load("assets/sprites/bird/yellowbird-downflap.png"),
    pygame.image.load("assets/sprites/bird/yellowbird-midflap.png"),
    pygame.image.load("assets/sprites/bird/yellowbird-upflap.png")

]

animationsList = [BLUE_BIRD_ANIMATION, RED_BIRD_ANIMATION, YELLOW_BIRD_ANIMATION]

# !!!! Dynamic objects !!!!
DELTA_X = 1

# Pipes
PIPE_GREEN_IMG = pygame.image.load("assets/sprites/Pipe/pipe-green.png")
PIPE_RED_IMG = pygame.image.load("assets/sprites/Pipe/pipe-red.png")

PIPES_IMG_LIST = [PIPE_GREEN_IMG, PIPE_RED_IMG]

PIPE_WIDTH = PIPE_GREEN_IMG.get_width()
GAP_SIZE = (PIPE_WIDTH, BIRD_SIZE[1] * 4)

INITIAL_PIPES_X_POSE = WINDOW_WIDTH + PIPE_WIDTH / 2
INITIAL_PIPES_Y_MAX_POSE = 320
INITIAL_PIPES_Y_MIN_POSE = 100
GENERATION_TIME = 3.0

WINDOW_BACKGROUND_COLOR = "White"

# !!!! Horizon !!!!
HORIZON_IMAGE = pygame.image.load("assets/sprites/Background/base.png")
HORIZON_WIDTH = HORIZON_IMAGE.get_width()
HORIZON_HEIGHT = HORIZON_IMAGE.get_height()

# !!!! Background !!!!
BACKGROUND_DAY_IMAGE = pygame.image.load("assets/sprites/Background/background-day.png")
BACKGROUND_NIGHT_IMAGE = pygame.image.load("assets/sprites/Background/background-night.png")
BACKGROUND_IMAGE_LIST = [BACKGROUND_DAY_IMAGE, BACKGROUND_NIGHT_IMAGE]