import json
import glob
import numpy
from music21 import converter, instrument, note, chord
from numpy import array
from numpy import ndarray
from numpy import hstack
from keras.utils import np_utils

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import MaxPooling1D
from tensorflow.keras.layers import Conv1D
from keras.callbacks import History
from typing import Tuple, Dict, Union, List

def get_model( X, y, parameters: Dict[str, Union[str, int, float]]) -> Sequential:

    """
    :param x: list of the groups with selected size sequences 
    :param y: array of next values of each squence group
    :param parameters: - dict with the model configs

    :return: A tuple with a model and history that can be used to generate graphs
    """
    n_features = X.shape[2]

    model = Sequential()
    model.add(Conv1D(filters=parameters['filters'], kernel_size=parameters['kernel_size'], activation=parameters['activation']))
    model.add(MaxPooling1D(pool_size=parameters['pool_size']))
    model.add(Flatten())
    model.add(Dense(parameters['dense_units'], activation=parameters['activation']))
    model.add(Dense(n_features))
    model.compile(optimizer=parameters['optimizer'], loss=parameters['loss'])

    model.compile(optimizer=parameters['optimizer'], loss=parameters['loss'])
    model.fit(X.astype(numpy.float32), y.astype(numpy.float32), epochs=parameters['epochs'], verbose=parameters['verbose'])
    return model

def get_model_inputs(in_seq1, in_seq2, n_steps):
    def split_sequences(sequences, n_steps):
        X, y = list(), list()
        for i in range(len(sequences)):
            end_ix = i + n_steps
            if end_ix > len(sequences)-1:
                break
            seq_x, seq_y = sequences[i:end_ix, :], sequences[end_ix, :]
            X.append(seq_x)
            y.append(seq_y)
        return array(X), array(y)
    in_seq1 = in_seq1.reshape((len(in_seq1), 1))
    in_seq2 = in_seq2.reshape((len(in_seq2), 1))
    dataset = hstack((in_seq1, in_seq2))

    X, y = split_sequences(dataset, n_steps)
    return X, y
