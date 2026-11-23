'''
This module contains the Artificial Intelligence model that will play the game.
The model is made with three important libraries: keras and tensor flow.
It consists of a neural network of 5 input variables, 1 hidden layer of 8 neurons (ReLu activation)
and 2 outputs.

The inputs are: y bird position, bird y velocity, obstacle x distance, gap y position and gap y distance
The outputs are: jump probability vs do nothing probability

The train method is evolutive. We set several birds play, and then we select the one with the best score.
Then we clone the best bird several times and mutate each of its children. We repeat this cycle until
we get an efficient model.
'''
from asyncio import constants

import tensorflow as tf
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers

class Neural_Network:
    def __init__(self):
        self.model = keras.Sequential([
            # Hidden ReLu layers
            layers.Dense(units=8, activation='relu', input_shape=[5]),
            layers.Dense(units=8, activation='relu'),
            # Output layer
            layers.Dense(units=1, activation='sigmoid')
        ])

    @tf.function
    def predict(self, x):
        prediction = self.model(x, training=False)

        return prediction

    # Mutate the weights and biases of each layer of the neural network
    # The first parameter "learningRate" refers to the intensity of mutation
    # that our weight can experiment.
    # The second parameter is the probability of each parameter to be mutated
    # with a logic mask.

    def mutate(self, learningRate, probability):
        for layer in self.model.layers:
            weights = layer.get_weights()

            # skip the layer if it doesn't have any weights
            if len(weights) == 0:
                continue

            W, b = weights

            # Probability mask
            wMask = np.random.random(W.shape) < probability
            bMask = np.random.random(b.shape) < probability

            # Gaussian distribution noise
            wNoise = np.random.normal(0, learningRate, W.shape)
            bNoise = np.random.normal(0, learningRate, b.shape)

            # Mutate the weights
            W += wNoise * wMask
            b += bNoise * bMask

            # Apply the mutation to the neural net
            layer.set_weights([W, b])

    def saveModel(self, path="best_model.keras"):
        self.model.save(path)
        print("model saved correctly")

    @staticmethod
    def loadModel(path="best_model.keras"):
        nn = Neural_Network()
        nn.model = keras.models.load_model(path)

        return nn

