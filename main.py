import pygame

import constants
from bird.Bird import Bird

# pygame setup
pygame.init()
window = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
clock = pygame.time.Clock()
running = True
startGame = False

# !!!! Create Bird !!!!
bird = Bird(constants.WINDOW_WIDTH/2, constants.WINDOW_HEIGHT/2)

birdGroup = pygame.sprite.Group()
birdGroup.add(bird)

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
                bird.jump()

    # !!!! Render the game !!!!

    # Draw elements
    birdGroup.draw(window)

    if startGame:
        # Update elements
        birdGroup.update()

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()