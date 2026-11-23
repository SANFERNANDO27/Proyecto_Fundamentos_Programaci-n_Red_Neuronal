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
import tensorflow as tf
import constants
from pygame import Rect

from pygame.sprite import Sprite
from neural_network.Neural_Network import Neural_Network
from tensorflow.python.framework.test_ops import none
from utils.Utils import Timer


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y, neuralNetwork =None):
        # Define neural network
        if neuralNetwork is None:
            self.neuralNetwork = Neural_Network()
        else:
            self.neuralNetwork = neuralNetwork

        pygame.sprite.Sprite.__init__(self)
        # Define animation
        self.animation = random.choice(constants.animationsList) # Select a random animation
        self.frameIndex = 0
        self.timer = Timer()
        self.framesAlive = 0
        self.score = 0 # Fitness 1, the score
        self.bestYDistance = 1000 # Fitness 2, the y distance to the gap

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
        # also the bird only can jump if delta y is negative, so the nn cannot spam the jump
        if self.alive and self.delta_y > 0:
            self.delta_y = -constants.JUMPING_VELOCITY
            #self.jumpSound.play()

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

        # Iterate for each gap to detect a collision
        for gap in gapGroup:
            # Check if the bird is alive to avoid sum a point when falling in the dead effect
            if self.hitbox.colliderect(gap.rect) and self.alive:
                # gain score if we pass through the gap
                self.score += 1
                self.pointSound.play()
                # Kill the gap to avoid obtaining more than 1 point
                gap.kill()

    # Verify that the bird does not exceed the sky or the horizon
    # In case that the bird over-escapes any of those, trigger the game over
    def verifyLimits(self):
        yPosition = self.rect.center[1]
        if yPosition > 390 or yPosition < -25:
            self.gameOver()

        # Delete the bird if it falls out the window
        if yPosition > constants.WINDOW_HEIGHT:
            self.kill()

    # This function draws the rect and hitbox of the bird.
    # It is not normally used in the game, is only made for debugging and for
    # visualize the areas.
    def draw(self, window):
        pygame.draw.rect(window, "red", self.rect)
        pygame.draw.rect(window, "green", self.hitbox)

    def reset(self, x, y):
        # Revive
        self.alive = True

        # Reset position
        self.rect.center = (x, y)

        # Reset y velocity
        self.delta_y = 0

        # Reset animation
        frame = self.animation[0]
        self.image = pygame.transform.rotate(frame, 0)

        # Reset score
        self.score = 0

    def getScore(self):
        return self.score

    # Get the fitness: 100score + 0.1f + K/(1 + d)
    # Where score are the points of the bird, f the frames survived, K is the proximity recompence and d is the y gap distance
    def getFitness(self):
        score = self.getScore()
        frames = self.framesAlive
        yDistance = self.bestYDistance
        K = 10

        fitness = (
            score * 100 +
            frames * 0.1 +
            K / (1 + yDistance)
        )

        return fitness

    def isAlive(self):
        return self.alive

    # Neural Network variables
    def getYPosition(self):
        return self.rect.centery

    def getXPosition(self):
        return self.rect.x

    def getYVelocity(self):
        return self.delta_y

    # Returns the x position of the closest obstacle and the x distance between the bird and the obstacle as a tupple
    # The x referene point of the pipe is the left, this to let the nn identify when the bird leaves the pipe
    # Format: closestObstacleXPosition, closestDistance
    # If the obstacle group is empty, returns 2 zeros: 0, 0
    def getClosestObstacle(self, obstacleGroup):
        # Verify if we have obstacles
        if len(obstacleGroup) > 0:
            closestObstacleXPosition = 0
            closestDistance = float("inf")  # An irreal initial distance to always replace it (window width)

            # Find the closest obstacle by x distance
            # The distance can not be 0 to avoid the nn detect pipes at the back
            for obstacle in obstacleGroup:
                distance = obstacle.rect.centerx - self.getXPosition()

                if distance > 0 and distance < closestDistance:
                    # Define closest obstacle
                    closestObstacleXPosition = obstacle.rect.centerx
                    closestDistance = distance

            return closestObstacleXPosition, closestDistance

        return 0.0, 0.0

    # Returns the y position of the closest gap and the y distance between the bird and the gap as a tupple
    # The y referene point of the gap is the center
    # Format: closestGapYPosition, closestDistance
    # If the gap group is empty, returns 2 zeros: 0, 0
    def getClosestGap(self, gapGroup):

        closestGap = None
        closestXDistance = float("inf")

        for gap in gapGroup:

            xDistance = gap.rect.centerx - self.rect.centerx

            if xDistance >= 0 and xDistance < closestXDistance:
                closestXDistance = xDistance
                closestGap = gap

        if closestGap is None:
            return constants.WINDOW_HEIGHT / 2, constants.WINDOW_HEIGHT / 2

        gapY = closestGap.rect.centery
        yDistance = gapY - self.rect.centery

        return gapY, yDistance

    # Get the neural network of the bird
    def getNeuralNetwork(self):
        return self.neuralNetwork

    # This is the function that we call in the main module for execute all the
    # other important physics and animations functions
    def update(self, window, obstacleGroup, gapGroup):
        self.updateAnimation()
        self.gravity()
        self.verifyCollision(obstacleGroup, gapGroup)
        self.verifyLimits()

        # Neural Network control

        # Define and preprocess inputs
        obstacleXPosition, obstacleXDistance = self.getClosestObstacle(obstacleGroup)
        gapYPosition, gapYDistance = self.getClosestGap(gapGroup)

        # The inputs are: y bird position, y bird velocity, obstacle x distance, gap y position and gap y distance
        # Divide over window width and height to mantain the input variables between -1 and 1

        inputs = tf.convert_to_tensor([
                [self.rect.centery / constants.WINDOW_HEIGHT,
                 self.delta_y / 100,
                 obstacleXDistance / constants.WINDOW_WIDTH,
                 gapYPosition / constants.WINDOW_HEIGHT,
                 gapYDistance / constants.WINDOW_HEIGHT]
            ], dtype=tf.float32)

        # Predict the action
        prediction = self.neuralNetwork.predict(inputs)
        prediction = prediction.numpy()[0][0]

        # Define the action
        # If the prediction is more than 0.5, then the bird jump; else the bird falls
        if prediction >= 0.5:
            self.jump()

        # Define the fitness, in this case the absolute gapYDistance
        # This will help us find the birds that were more closer to pass trough a gap
        # We only do this when the bird is alive
        if self.alive:
            self.bestYDistance = min(self.bestYDistance, abs(gapYDistance))
            self.framesAlive += 1 # Update the frames alive

        else:
            # game over spinning effect
            self.deadAngle -= 5
            self.image = pygame.transform.rotate(self.animation[0], self.deadAngle)

