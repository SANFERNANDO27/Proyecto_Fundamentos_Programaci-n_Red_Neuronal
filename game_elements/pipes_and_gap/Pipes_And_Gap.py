import random
import pygame
import constants
from game_elements.dynamic_object.Dynamic_Object import Dynamic_Object


class Pipes_And_Gap:
    def __init__(self, x, pipesGroup: pygame.sprite.Group):
        # Create the gab
        gapYCenter = random.randint(200, 300)
        gapSurface = pygame.Surface(constants.GAP_SIZE, pygame.SRCALPHA)

        self.gap = Dynamic_Object(x, gapYCenter, gapSurface)

        # Create pipes
        pipeImg = constants.PIPE_IMG
        upperPipeImg = pygame.transform.flip(pipeImg, False, True)

        self.upperPipe = Dynamic_Object(x, 0, upperPipeImg)
        self.lowerPipe = Dynamic_Object(x, 0, pipeImg)

        # Set pipes positions
        self.upperPipe.rect.bottom = self.gap.rect.top
        self.lowerPipe.rect.top = self.gap.rect.bottom

        # Add the dynamic object to the sprite group
        pipesGroup.add(self.gap)
        pipesGroup.add(self.upperPipe)
        pipesGroup.add(self.lowerPipe)