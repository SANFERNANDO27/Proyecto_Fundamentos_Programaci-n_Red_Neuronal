import random
import pygame
import constants
from game_elements.dynamic_object.Dynamic_Object import Dynamic_Object


class Pipes_And_Gap(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()

        # Create the gab
        gapYCenter = random.randint(200, 300)
        gapSurface = pygame.Surface(constants.GAP_SIZE, pygame.SRCALPHA)

        self.gap = Dynamic_Object(x, gapYCenter, gapSurface)

        self.image = self.gap.image
        self.rect = self.gap.image.get_rect()

        # Create pipes
        pipeImg = constants.PIPE_IMG
        upperPipeImg = pygame.transform.flip(pipeImg, False, True)

        self.upperPipe = Dynamic_Object(x, 0, upperPipeImg)
        self.lowerPipe = Dynamic_Object(x, 0, pipeImg)

        # Set pipes positions
        self.upperPipe.rect.bottom = self.gap.rect.top
        self.lowerPipe.rect.top = self.gap.rect.bottom

    def draw(self, window):
        self.gap.draw(window)
        self.upperPipe.draw(window)
        self.lowerPipe.draw(window)

    def update(self, window):
        self.draw(window)
        self.gap.update()
        self.upperPipe.update()
        self.lowerPipe.update()