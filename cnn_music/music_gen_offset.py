import tensorflow as tf 
from tensorflow import keras
from tensorflow.keras.models import Sequential
import pickle, argparse, sys, json, note
from music21 import stream
from numpy import hstack
from numpy import array
import numpy

input_parser = argparse.ArgumentParser('Given an input generates music')
input_parser.add_argument('-md','--midi',
        metavar='input.mid',
        type=str,
        help='path to input midi; input.mid assumed if not specifyed'
        )
input_parser.add_argument('-o','--output',
        metavar='output.mid',
        type=str,
        help='path to output; results/output.mid assumed if not specifyed'
        )
input_parser.add_argument('-ml','--model',
        metavar='model',
        type=str,
        help='path to model; models/model assumed if not specifyed'
        )

args = input_parser.parse_args()
input_predict = args.midi if args.midi else 'inputs/1_input.mid'
train_output_file = open(args.model,'rb') if args.model else open("models/modelOffSett",'rb')
output_file_path = args.output if args.output else 'results/output_offset.mid'

model = keras.models.load_model("models/modelOffSet")

train_output = pickle.load(train_output_file)
pitchnames = train_output['pitchnames']
n_steps = train_output['groups_size']
n_features = train_output['n_features']

data_input_predict = note.get_notes_info(input_predict);
x_input_notes = note.get_int_notes(pitchnames, data_input_predict['notes'])
x_input_offsets = data_input_predict['offsets']
x_input = [[x_input_notes[i], x_input_offsets[i]] for i in range(n_steps)]

new_series = x_input;
x_input = array(x_input);
x_input = x_input.reshape((1, n_steps, n_features))
last_offset = 0
    
for i in range(n_steps):
    yhat = model.predict(x_input.astype(numpy.float32), verbose=0)
    offset_diff = yhat[0][1] - last_offset
   
    if offset_diff < 0:
        yhat[0][1] = last_offset + 0.5
    
    last_offset = yhat[0][1]
    new_series = new_series[1:n_steps]
    new_series.append(yhat[0])
    
    x_input = new_series
    x_input = array(x_input);
    x_input = x_input.reshape((1, n_steps, n_features))
    
int_notes = [ round(prediction[0]) if prediction[0] >= 0 else 0 for prediction in new_series ]
int_notes = [ n if n < len(pitchnames) else len(pitchnames) -1 for n in int_notes]
first_offset = new_series[0][1]
offsets = [ prediction[1] - first_offset  for prediction in new_series ]
int_to_note = dict((number, note) for number, note in enumerate(pitchnames))
notes_strs = note.get_note_strings(int_to_note, int_notes)
notes_list = note.get_notes_chords_list_offset(notes_strs, offsets)
print(offsets)
midi_stream = stream.Stream(notes_list)
midi_stream.write('midi', fp=output_file_path)
