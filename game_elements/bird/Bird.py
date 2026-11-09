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
        self.score = 0

        # Define img
        self.image = self.animation[self.frameIndex]

        # Define sound effects
        self.jumpSound = pygame.mixer.Sound("assets/audio/wing.wav")
        self.pointSound = pygame.mixer.Sound("assets/audio/point.wav")
        self.dieSound = pygame.mixer.Sound("assets/audio/die.wav")
        self.hitSound = pygame.mixer.Sound("assets/audio/hit.wav")


        # Define and configure rect
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Define and configure the hitbox of the bird (smaller than the image rect)
        self.hitbox = pygame.Rect(x, y, constants.BIRD_HIT_BOX_SIZE_X, constants.BIRD_HIT_BOX_SIZE_Y)

        # Y velocity of the bird
        self.delta_y = 0

        # Alive
        self.alive = True
        self.deadAngle = 0

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
            self.jumpSound.play()

    # This function control the gravity, so if the player
    # doesn't jump, the bird falls with constant acceleration.
    def gravity(self):
        self.delta_y += constants.GRAVITY

        # Max velocity 10 px/sec
        self.rect.y += min(self.delta_y, 10)

        # Center the hitbox to the image rect
        self.hitbox.center = self.rect.center

    # Kill the bird and trigger the game over sound
    def gameOver(self):
        if self.alive:
            self.hitSound.play()
            self.dieSound.play()

        self.alive = False

    # This function detects other elements that are in the parameter list.
    # If it detects an obstacle, the bird dies. If it detects a gap the score
    # increase by 1.
    def verifyCollision(self, obstacleGroup, gapGroup):
        # Iterate for each obstacle to detect a collision
        for obstacle in obstacleGroup:
            if self.hitbox.colliderect(obstacle.rect):
                # Kill the bird in case of collision
                self.gameOver()
                #self.kill()

        # Iterate for each gap to detect a collision
        for gap in gapGroup:
            if self.hitbox.colliderect(gap.rect) and self.alive:
                # gain score if we pass through the gap
                self.score += 1
                self.pointSound.play()
                # Kill the gap to avoid obtaining more than 1 point
                gap.kill()

    # Verify that the bird does not exceed the sky or the horizon
    # In case that the bird over-escapes any of those, trigger the game over
    def verifyLimits(self):
        if self.rect.center[1] > 390 or self.rect.center[1] < -25:
            self.gameOver()

    # This function draws the rect and hitbox of the bird.
    # It is not normally used in the game, is only made for debugging and for
    # visualize the areas.
    def draw(self, window):
        pygame.draw.rect(window, "red", self.rect)
        pygame.draw.rect(window, "green", self.hitbox)

    def getScore(self):
        return self.score

    # This is the function that we call in the main module for execute all the
    # other important physics and animations functions
    def update(self, window, obstacleGroup, gapGroup):
        #self.draw(window)
        self.updateAnimation()
        self.gravity()
        self.verifyCollision(obstacleGroup, gapGroup)
        self.verifyLimits()

        # game over spinning effect
        if not self.alive:
            self.deadAngle -= 5
            self.image = pygame.transform.rotate(self.animation[0], self.deadAngle)

