import json
import glob
import numpy
from music21 import converter, instrument, note, chord
from numpy import array
from numpy import ndarray
from keras.utils import np_utils

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import MaxPooling1D
from tensorflow.keras.layers import Conv1D
from keras.callbacks import History
from typing import Tuple, Dict, Union, List

def get_model( x, y, parameters: Dict[str, Union[str, int, float]]) -> Sequential:

    """
    :param x: list of the groups with selected size sequences 
    :param y: array of next values of each squence group
    :param parameters: - dict with the model configs

    :return: A tuple with a model and history that can be used to generate graphs
    """
    n_features = x.shape[2]
    model = Sequential()
    model.add(
        Conv1D(
            filters=parameters["filters"],
            kernel_size=parameters["kernel_size"],
            activation=parameters["activation"],
            input_shape = (parameters['groups_size'], n_features)
        )
    )
    model.add(MaxPooling1D(pool_size=parameters["pool_size"]))
    model.add(Flatten())
    model.add(Dense(parameters["dense_units"], activation=parameters['activation']))
    model.add(Dense(n_features))
    model.compile(
        optimizer=parameters["optimizer"],
        loss=parameters["loss"],
        metrics=["mae", "accuracy"],
    )
    return model

def get_model_inputs(in_seq1, in_seq2, n_steps):
    in_seq1 = in_seq1.reshape((len(in_seq1), 1))
    in_seq2 = in_seq2.reshape((len(in_seq2), 1))
    dataset = hstack((in_seq1, in_seq2))

    X, y = split_sequences(dataset, n_steps)
    return X, y
