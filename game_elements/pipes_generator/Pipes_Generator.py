import pygame

import constants
import random
from game_elements.pipes_and_gap.Pipes_And_Gap import Pipes_And_Gap
from utils.Utils import Timer


class Pipes_Generator:
    def __init__(self):
        self.timer = Timer()
        self.pipesGroup = pygame.sprite.Group()
        self.pipeImg = random.choice(constants.PIPES_IMG_LIST) # Select a random pipe color

    def generate(self):
        if self.timer.get_seconds() > constants.GENERATION_TIME:
            Pipes_And_Gap(constants.INITIAL_PIPES_X_POSE, self.pipesGroup, self.pipeImg)
            self.timer.reset()

    def draw(self, window):
        self.pipesGroup.draw(window)

    def update(self):
        self.timer.update()
        self.generate()
        self.pipesGroup.update()


