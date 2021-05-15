from music21 import instrument, stream, note, chord
import numpy
from numpy import array
from numpy import ndarray
from keras.utils import np_utils
from keras.models import load_model
from keras.models import Sequential
from typing import List

def predict_next(x_input: ndarray, model: Sequential, set_size: int) -> int:
    """
    :param x_input: a time series 
    :param model: a keras Sequential model
    :param set_size: size of notes set 

    :return: the predicted next number on series 
    """
    next_value = model.predict(x_input.astype(numpy.float32),verbose =0 )
    next_value = next_value.tolist()[0][0]
    next_value = round(next_value)
    if next_value < 0:
        next_value = 0
    elif next_value >= set_size:
        next_value = set_size - 1
    return next_value 

def get_new_series(size: int, input, model, set_size: int) -> List[int]:
    """
    :param size: the size of output series 
    :param model: a keras Sequential model
    :param set_size: size of notes set 

    :return: number series with length size
    """
    new_series = input.tolist()
    x_input = array(new_series)
    x_input = x_input.reshape((1,size,1))
    for i in range(0,size):
        predicted = predict_next(x_input, model, set_size)
        new_series = new_series[1:size]
        new_series.append(predicted)
        x_input = array(new_series)
        x_input = x_input.reshape((1,size,1))
    return new_series

def get_new_series_offset(size: int, input, model) -> List[int]:
    """
    :param size: the size of output series 
    :param model: a keras Sequential model
    

    :return: number series with length size
    """
    new_series = input.tolist()
    x_input = array(new_series)
    x_input = x_input.reshape((1,size,1))
    last_offset = 0
    cont=0
    for i in range(0,size):
        yhat = model.predict(x_input.astype(numpy.float32), verbose=0)
        offset_diff = yhat - last_offset
   
        if offset_diff < 0:
            yhat = last_offset + 0.5
            cont=cont+1
    
        last_offset = yhat
        new_series = new_series[1:size]
        new_series.append(yhat)
    
        x_input = new_series
        x_input = array(x_input);
        x_input = x_input.reshape((1,size,1))
    return new_series