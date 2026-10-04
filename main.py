'''
This module contains the main class.
This class has the intention to bring together all the game elements.
It also manages the window, the button bindings, the game score and
the game flow.

This module haves some important libraries, the first is the pygame
library, that manages the window creation, the sprites, animations
and clock.
The last one is the python native library, random. This last one
only works for select the background theme.
'''

import pygame

import constants
import random
from game_elements.bird.Bird import Bird
from game_elements.dynamic_object.Dynamic_Object import BackgroundDynamicImage
from game_elements.pipes_generator.Pipes_Generator import Pipes_Generator

# pygame setup (window, clock and flow variables)
pygame.init()
window = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
clock = pygame.time.Clock()

# This variable control the window flow, if true the window will run.
running = True

# This variable control the game flow, if true the game will begin.
startGame = False

# !!!! Create Bird !!!!
bird = Bird(constants.WINDOW_WIDTH / 2, constants.WINDOW_HEIGHT / 2)

# Create the bird list (this is made like this to make easier the Neural Network training)
birdGroup = pygame.sprite.Group()
birdGroup.add(bird)

# !!!! Create Background !!!!
# Select randomly between two background images (day and night)
backgroundImage = random.choice(constants.BACKGROUND_IMAGE_LIST) # Select random background (day or night)
background = BackgroundDynamicImage(backgroundImage)


# !!!! Create Horizon !!!!
horizon = BackgroundDynamicImage(constants.HORIZON_IMAGE)

# !!!! Pipe generator !!!!
pipesGenerator = Pipes_Generator()

while running:
    # fill the screen with a color to wipe away anything from last frame
    window.fill(constants.WINDOW_BACKGROUND_COLOR)

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                startGame = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if not startGame:
                    startGame = True

                bird.jump()

    # !!!! Render the game !!!!

    # Draw elements
    background.draw(window)
    pipesGenerator.draw(window)
    horizon.draw(window)
    birdGroup.draw(window)

    if startGame:
        # Update elements
        background.update()
        pipesGenerator.update()
        horizon.update()
        birdGroup.update(window, pipesGenerator.getPipesGroup())

    # !!!! Game Over if the bird collide with a pipe !!!!

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()