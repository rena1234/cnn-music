from music21 import instrument, stream, note, chord
import numpy
from numpy import array
from numpy import ndarray
from keras.utils import np_utils
from keras.models import load_model
from keras.models import Sequential
from typing import List

def predict_next(x_input, model: Sequential, set_size: int) -> int:
    """
    :param x_input: a time series 
    :param model: a keras Sequential model
    :param set_size: size of notes set 

    :return: the predicted next number on series 
    """
    input = array(x_input).astype(numpy.float32)
    input = input.reshape((1, 100, 2))
    next_value = model.predict(input,verbose =0 )
    next_value = next_value.tolist()[0]
    return next_value 

def get_new_series(size: int, input, model, set_size: int) -> List[int]:
    """
    :param size: the size of output series 
    :param model: a keras Sequential model
    :param set_size: size of notes set 

    :return: number series with length size
    """
    new_series = input
    x_input = new_series
    for i in range(0,size):
        predicted = predict_next(x_input, model, set_size)
        new_series = new_series[1:size]
        new_series.append(predicted)
        x_input = array(new_series)
    return new_series

def get_new_series_offset(size: int, input, model, set_size: int):
    """
    :param size: the size of output series 
    :param model: a keras Sequential model
    :param set_size: size of notes set 

    :return: number series with length size
    """
    new_series = input
    x_input = new_series
    for i in range(0,size):
        predicted = predict_next(x_input, model, set_size)
        new_series = new_series[1:size]
        new_series.append(predicted)
        x_input = new_series
    return new_series
    

def get_prediction_input(
    int_notes: List[int], offsets, sequence_length: int, 
):
    """
    :param int_notes: sequence of notes converted to integers 
    :param sequence_length: size of the grouped series 

    :return: tuple with list of series groups, and next value to each group 
    """
    return [ [int_notes[i], offsets[i]] for i in range(0, sequence_length)]
