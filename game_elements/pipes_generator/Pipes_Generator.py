import pygame

import constants
import random
from game_elements.dynamic_object.Dynamic_Object import Dynamic_Object
from utils.Utils import Timer

class Pipes_And_Gap:
    def __init__(self, x,
                 pipesGroup: pygame.sprite.Group,
                 gapsGroup: pygame.sprite.Group,
                 pipeImg: pygame.sprite.Group):
        # Create the gab
        gapYCenter = random.randint(constants.INITIAL_PIPES_Y_MIN_POSE, constants.INITIAL_PIPES_Y_MAX_POSE)
        gapSurface = pygame.Surface(constants.GAP_SIZE, pygame.SRCALPHA)
        #gapSurface.fill("Green")

        self.gap = Dynamic_Object(x, gapYCenter, gapSurface)

        # Create pipes
        upperPipeImg = pygame.transform.flip(pipeImg, False, True)

        self.upperPipe = Dynamic_Object(x, 0, upperPipeImg)
        self.lowerPipe = Dynamic_Object(x, 0, pipeImg)

        # Set pipes positions
        self.upperPipe.rect.bottom = self.gap.rect.top
        self.lowerPipe.rect.top = self.gap.rect.bottom

        # Add the dynamic object to the sprite group
        gapsGroup.add(self.gap)
        pipesGroup.add(self.upperPipe)
        pipesGroup.add(self.lowerPipe)

class Pipes_Generator:
    def __init__(self):
        self.timer = Timer()
        self.pipesGroup = pygame.sprite.Group()
        self.gapsGroup = pygame.sprite.Group()
        self.pipeImg = random.choice(constants.PIPES_IMG_LIST) # Select a random pipe color

    def generate(self):
        if self.timer.get_seconds() > constants.GENERATION_TIME:
            Pipes_And_Gap(constants.INITIAL_PIPES_X_POSE, self.pipesGroup,  self.gapsGroup, self.pipeImg)
            self.timer.reset()

    def draw(self, window):
        self.pipesGroup.draw(window)
        self.gapsGroup.draw(window)

    def reset(self):
        self.pipesGroup.empty()
        self.gapsGroup.empty()
        self.timer.reset()

    def update(self):
        self.timer.update()
        self.generate()
        self.pipesGroup.update()
        self.gapsGroup.update()

    def getPipesGroup(self):
        return self.pipesGroup

    def getGapsGroup(self):
        return self.gapsGroup


