import pygame
import math
import random

from pygame.sprite import Sprite

import constants
from utils.Utils import Timer


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # Define animation
        self.animation = random.choice(constants.animationsList) # Select a random animation
        self.frameIndex = 0
        self.timer = Timer()

        # Define img
        self.image = self.animation[self.frameIndex]

        # Define and configure rect
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Jumping and Gravity
        self.delta_y = 0
        self.jumping = False

        # Alive
        self.alive = True

    def updateAnimation(self):
        # Fly animation
        frame = self.animation[self.frameIndex]

        if self.timer.get_millie_seconds() > constants.BIRD_ANIMATION_COOLDOWN:
            self.frameIndex += 1
            self.timer.reset()

        if self.frameIndex == len(self.animation):
            self.frameIndex = 0

        self.timer.update()

        # Bird Rotation
        angle = -math.degrees(math.atan2(self.delta_y, constants.BIRD_DELTA_X)) # Find the angle trigonometry (Imaginary x velocity)
        angle = max(constants.MIN_BIRD_ANGLE, min(angle, constants.MAX_BIRD_ANGLE)) # Apply limits

        self.image = pygame.transform.rotate(frame, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def jump(self):
        # The bird can jump only if is alive
        if self.alive:
            self.delta_y = -constants.JUMPING_VELOCITY

    def set_jump(self):
        self.jumping = True

    def gravity(self):
        self.delta_y += constants.GRAVITY

        # Max velocity 10 px/sec
        self.rect.y += min(self.delta_y, 10)

    def verifyCollision(self, obstacleGroup):
        if pygame.sprite.spritecollide(self, obstacleGroup, False):
            self.alive = False
            #self.kill()

    def draw(self, window):
        pygame.draw.rect(window, "red", self.rect)

    def update(self, window, obstacleGroup):
        #self.draw(window)
        self.updateAnimation()
        self.gravity()
        self.verifyCollision(obstacleGroup)

