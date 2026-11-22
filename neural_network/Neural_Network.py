'''
This module contains the Artificial Intelligence model that will play the game.
The model is made with three important libraries: keras and tensor flow.
It consists of a neural network of 5 input variables, 2 hidden layers of 16 neurons (ReLu activation)
and 2 outputs.

The inputs are: y bird position, obstacle x position, obstacle x distance, gap y position and gap y distance
The outputs are: jump probability vs do nothing probability

The train method is evolutive. We set several birds play, and then we select the one with the best score.
Then we clone the best bird several times and mutate each of its children. We repeat this cycle until
we get an efficient model.
'''

import tensorflow as tf
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers

class Neural_Network:
    def __init__(self):
        self.model = keras.Sequential([
            # Hidden ReLu layers
            layers.Dense(units=16, activation='relu', input_shape=[5]),
            layers.Dense(units=16, activation='relu'),
            # Output layer
            layers.Dense(units=1, activation='sigmoid')
        ])

    @tf.function
    def predict(self, x):
        prediction = self.model(x, training=False)

        return prediction

