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

def get_model(
    x: ndarray, y: ndarray, parameters: Dict[str, Union[str, int, float]]
) -> Sequential:

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
    """
    history = model.fit(
        x,
        y,
        epochs=parameters["epochs"],
        verbose=parameters["verbose"],
        validation_split=parameters["validation"],
    )
    return model, history
    """
    return model

def get_model_inputs(
    int_notes: List[int], offsets, sequence_length: int, 
) -> Tuple[List[int], List[int]]:
    """
    :param int_notes: sequence of notes converted to integers 
    :param sequence_length: size of the grouped series 

    :return: tuple with list of series groups, and next value to each group 
    """
    """
    network_input = []
    network_output = []
    """
    network_input = list()
    network_output = list()
    for i in range(0, len(int_notes) - sequence_length):
        notes_sample = int_notes[i : i + sequence_length]
        offsets_sample = offsets[i : i + sequence_length] 
        network_input.append([[notes_sample[j], offsets_sample[j]] for j in range(0, sequence_length)])
        network_output.append([int_notes[i + sequence_length], offsets[i + sequence_length]])
        """
        network_input.append(int_notes[i : i + sequence_length])
        network_output.append(int_notes[i + sequence_length])
        """
    return network_input, network_output
