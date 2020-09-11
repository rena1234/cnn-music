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

    """
    print('INPUTANTESPREDICT--------------------')
    print(x_input)
    print('INPUTANTESPREDICT--------------------')
    """

    input = array(x_input).astype(numpy.float32)
    #input = numpy.asarray(x_input).astype(numpy.float32)
    #input = numpy.asarray(x_input)
    #input = x_input.astype(numpy.float32)
    #input = x_input
    input = input.reshape((1, 100, 2))
    next_value = model.predict(input,verbose =0 )
    next_value = next_value.tolist()[0]
    
    #next_value = round(next_value)
    """
    if next_value < 0:
        next_value = 0
    elif next_value >= set_size:
        next_value = set_size - 1
    """
    return next_value 

def get_new_series(size: int, input, model, set_size: int) -> List[int]:
    """
    :param size: the size of output series 
    :param model: a keras Sequential model
    :param set_size: size of notes set 

    :return: number series with length size
    """
    #new_series = input.tolist()
    new_series = input
    #x_input = array(new_series)
    x_input = new_series
    #x_input = x_input.reshape((1,size,1))
    for i in range(0,size):
        predicted = predict_next(x_input, model, set_size)
        new_series = new_series[1:size]
        new_series.append(predicted)
        x_input = array(new_series)
        #x_input = x_input.reshape((1,size,1))
    return new_series

def get_new_series_offset(size: int, input, model, set_size: int):
    """
    :param size: the size of output series 
    :param model: a keras Sequential model
    :param set_size: size of notes set 

    :return: number series with length size
    """
    #new_series = input.tolist()
    new_series = input
    #x_input = array(new_series)
    x_input = new_series
    #x_input = x_input.reshape((1,size,1))
    for i in range(0,size):
        predicted = predict_next(x_input, model, set_size)
        new_series = new_series[1:size]
        new_series.append(predicted)
        x_input = new_series
        #x_input = x_input.reshape((1,size,1))
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
    """
    network_input = list()
    for i in range(0, len(int_notes) - sequence_length):
        notes_sample = int_notes[i : i + sequence_length]
        offsets_sample = offsets[i : i + sequence_length] 
        network_input.append([notes_sample[j], offsets_sample[j]] for j in range(0, sequence_length))
        """

    return network_input
