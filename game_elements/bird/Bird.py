'''
This class is made for the main character of te game, the bird
It works as a pygame.Sprite child, so it needs and image, and a rect.
(A rect is a 2D geometric figure that describe the movement and collisions
of a game element)

This module includes 3 important libraries:
- pygame: for physics render and animations
- math: for some angle calculations
- random: to choice between tree sprites (blue, red or yellow bird)

The idea of the bird is that it only moves along the y-axis and all
the other game elements moves toward the bird. This creates and
effect that makes the player believe the bird is moving.
This method simplifies the physics calculations and memory.
'''

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

        # Define and configure the hitbox of the bird (smaller than the image rect)
        self.hitbox = pygame.Rect(x, y, constants.BIRD_HIT_BOX_SIZE_X, constants.BIRD_HIT_BOX_SIZE_Y)

        # Y velocity of the bird
        self.delta_y = 0

        # Alive
        self.alive = True

    # this function manage the frame control of the flying animation.
    # It also calculates the angle of the bird when is jumping or falling
    def updateAnimation(self):
        # Fly animation
        frame = self.animation[self.frameIndex]

        # If the timer exceeds the cooldown, we change the frame
        if self.timer.get_millie_seconds() > constants.BIRD_ANIMATION_COOLDOWN:
            self.frameIndex += 1
            self.timer.reset()

        # If the frame index exceeds the max frame len we come back to the first frame
        if self.frameIndex == len(self.animation):
            self.frameIndex = 0

        self.timer.update() # This method is essential for the timer to work

        # Bird Rotation
        angle = -math.degrees(math.atan2(self.delta_y, constants.BIRD_DELTA_X)) # Find the angle trigonometry (Imaginary x velocity)
        angle = max(constants.MIN_BIRD_ANGLE, min(angle, constants.MAX_BIRD_ANGLE)) # Apply angle limits

        # Rotate the image, but not the rect
        self.image = pygame.transform.rotate(frame, angle)

    # This function resets the delta y velocity.
    # This cancel the gravity for a moment and propels upwards the bird
    def jump(self):
        # The bird can jump only if is alive
        if self.alive:
            self.delta_y = -constants.JUMPING_VELOCITY

    # This function control the gravity, so if the player
    # doesn't jump, the bird falls with constant acceleration.
    def gravity(self):
        self.delta_y += constants.GRAVITY

        # Max velocity 10 px/sec
        self.rect.y += min(self.delta_y, 10)

        # Center the hitbox to the image rect
        self.hitbox.center = self.rect.center

    # This function detects other elements that are in the parameter list.
    # If it detects an obstacle, the bird dies. If it detects a gap the score
    # increase by 1.
    def verifyCollision(self, obstacleGroup):
        for obstacle in obstacleGroup:
            if self.hitbox.colliderect(obstacle.rect):
                self.alive = False
                #self.kill()

    # This function draws the rect and hitbox of the bird.
    # It is not normally used in the game, is only made for debugging and for
    # visualize the areas.
    def draw(self, window):
        pygame.draw.rect(window, "red", self.rect)
        pygame.draw.rect(window, "green", self.hitbox)

    # This is the function that we call in the main module for execute all the
    # other important physics and animations functions
    def update(self, window, obstacleGroup):
        #self.draw(window)
        self.updateAnimation()
        self.gravity()
        self.verifyCollision(obstacleGroup)

