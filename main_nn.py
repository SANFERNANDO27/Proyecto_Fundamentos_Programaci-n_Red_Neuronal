'''
This module is similar to the main class, with the difference that it spawns 50 birds to play simultaneously.
It also removes player controls and handles file saving and loading.

This module haves some important libraries:
- pygame: manages the window creation, the sprites, animations and clock.
- random: Manages some random operations.
- Copy: It is used to create copies of objects such that changes to these copies do not affect the original.
- os: It is used to check whether a file for a previously saved model exists.
'''
import pygame

import constants
import random
import copy
import os
from game_elements.bird.Bird_NN import Bird
from game_elements.dynamic_object.Dynamic_Object import BackgroundDynamicImage
from game_elements.pipes_generator.Pipes_Generator import Pipes_Generator
from utils.Utils import draw_text, scale_image
from neural_network.Neural_Network import Neural_Network

# pygame setup (window, clock and flow variables)
pygame.init()
pygame.mixer.init()
window = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
clock = pygame.time.Clock()

# This variable control the window flow, if true the window will run.
running = True

# This variable control the game flow, if true the game will begin.
startGame = False

# Images
getReadyImg = pygame.image.load("assets/sprites/Game_play/get_ready_message.png")
gameOverImg = pygame.image.load("assets/sprites/Game_play/game_over.png")
reloadButton = scale_image(pygame.image.load("assets/sprites/Game_play/reload_button.png"), 0.45)
reloadButton.set_alpha(240) # Change opacity

reloadButtonRect = reloadButton.get_rect(center=constants.RELOAD_BUTTON_POSITION)

# Reloud sound effect
reloadSound = pygame.mixer.Sound("assets/audio/swoosh.wav")

# !!!! Create Background !!!!
# Select randomly between two background images (day and night)
backgroundImage = random.choice(constants.BACKGROUND_IMAGE_LIST) # Select random background (day or night)
background = BackgroundDynamicImage(backgroundImage)


# !!!! Create Horizon !!!!
horizon = BackgroundDynamicImage(constants.HORIZON_IMAGE)

# !!!! Pipe generator !!!!
pipesGenerator = Pipes_Generator()

# !!!! Score variable !!!!
bestScore = 0
# !!!! Best neural network !!!!
bestFitness = 0
bestNN = None

# Create the bird list (this is made like this to make easier the Neural Network training)
birdsNum = 50
birdGroup = pygame.sprite.Group()

# Check if we have a saved model and load it
def loadModel():
    global bestNN

    nnDir = "neural_network"
    bestNNPath = constants.BEST_MODEL_PATH
    pathList = [nnDir, bestNNPath]

    path = "/".join(pathList)

    if os.path.exists(path):
        bestNN = Neural_Network.loadModel(path)
        print("Model loaded correctly")
    else:
        print("No model found")

# Create new birds and mutate their neural nets
def resetAndMutateBirds(birdGroup, birdsNum):
    learningRate = 0.05
    mutateProbability = 0.1
    elitism = 1 # The number of birds that will have the exactly same best nn without mutation

    for i in range(birdsNum):
        # Define a new neural network based on the best one
        nn = copy.deepcopy(bestNN)

        if i > elitism:
            nn.mutate(learningRate, mutateProbability)

        # Create the new bird
        bird = Bird(constants.WINDOW_WIDTH / 2, constants.WINDOW_HEIGHT / 2, nn)
        birdGroup.add(bird)

# Create new birds. If we have a saved model, we clone and mutate the nn.
# Else, we create new ones
def createBirds(birdGroup, birdsNum):
    if bestNN is None:
        for i in range(birdsNum):
            bird = Bird(constants.WINDOW_WIDTH / 2, constants.WINDOW_HEIGHT / 2)
            birdGroup.add(bird)
    else:
        resetAndMutateBirds(birdGroup, birdsNum)

# Check if the birds list is empty
def isBirdGroupEmpty():
    return len(birdGroup) == 0

# Draw the score on the top of the window
def drawScore():
    text = str(bestScore)
    draw_text(text, pygame.Color("Black"), constants.SCORE_TEXT_SIZE, constants.SCORE_TEXT_POSITION, window)

# Reset the game if all the birds die
def gameOver():
    resetGame()

# Reset and reload the game
def resetGame():
    global bestScore

    # Reset game elements state and create new birds
    resetAndMutateBirds(birdGroup, 50)
    pipesGenerator.reset()

    # Reset score
    bestScore = 0

    # play the reload sound effect
    reloadSound.play()

# Save the best neural network in keras format
def saveBestModel():
    nnDir = "neural_network"
    bestNNPath = constants.BEST_MODEL_PATH
    pathList = [nnDir, bestNNPath]

    path = "/".join(pathList)

    bestNN.saveModel(path)

# Find the best neural network
# It choose the models with the best score, with the most frame survived and those who were more close to pass through the gap
def setBestNeuralNetwork():
    global bestFitness, bestScore, bestNN

    for bird in birdGroup:
        fitness = bird.getFitness()
        score = bird.getScore()

        # Check if the bird have best score
        if fitness > bestFitness:
            # Set the new score record
            bestFitness = fitness
            bestScore = score
            # Update the new best nn
            bestNN = bird.getNeuralNetwork()

        #print(f"best fitness: {bestFitness}, fitness: {fitness}")

# Load model if exist
loadModel()

# !!!! Create Birds !!!!
createBirds(birdGroup, 50)

while running:
    # fill the screen with a color to wipe away anything from last frame
    window.fill(constants.WINDOW_BACKGROUND_COLOR)

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            saveBestModel()
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                startGame = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if not startGame:
                    startGame = True

            # Reload Button
            if reloadButtonRect.collidepoint(event.pos) and isBirdGroupEmpty():
                resetGame()

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
        birdGroup.update(window, pipesGenerator.getPipesGroup(), pipesGenerator.getGapsGroup())

        # Update score and draw score
        if not isBirdGroupEmpty(): # Only update if we have birds
            setBestNeuralNetwork() # Update best neural network

        drawScore()

        if isBirdGroupEmpty():
            gameOver()

    else:
        window.blit(getReadyImg, constants.GET_READY_IMG_POSITION)

    # !!!! Game Over if the bird collide with a pipe !!!!

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()