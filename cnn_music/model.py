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
import tensorflow as tf
import numpy as np

def get_model(x: ndarray, y: ndarray, parameters: Dict[str, Union[str,int,float]]) -> (Sequential, History):
    """
    :param x: list of the groups with selected size sequences 
    :param y: array of next values of each squence group
    :param parameters: - dict with the model configs

    :return: A tuple with a model and history that can be used to generate graphs
    """
    model = Sequential()
    model.add(Conv1D(filters=parameters['filters'], kernel_size= parameters['kernel_size'], activation= parameters['activation']) )
    model.add(MaxPooling1D(pool_size=parameters['pool_size']))
    model.add(Flatten())
    model.add(Dense(parameters['dense_units']))
    model.add(Activation(parameters['activation']))
    model.add(Dense(1))
    model.compile(optimizer=parameters['optimizer'], loss=parameters['loss'], metrics = ['mae', 'accuracy'])
    x = x.astype(np.float32)
    y = y.astype(np.float32)
    history = model.fit(x, y, epochs=parameters['epochs'], verbose=parameters['verbose'], validation_split=parameters['validation'])
    return model, history

def get_model_inputs(int_notes: List[int], sequence_length: int) -> Tuple[List[int], List[int]]:
    """
    :param int_notes: sequence of notes converted to integers 
    :param sequence_length: size of the grouped series 

    :return: tuple with list of series groups, and next value to each group 
    """
    network_input = []
    network_output = []
    for i in range(0, len(int_notes) - sequence_length):
        network_input.append(int_notes[i:i + sequence_length])
        network_output.append(int_notes[i + sequence_length])
    return network_input, network_output

