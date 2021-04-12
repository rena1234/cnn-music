import pickle
import sys
import tensorflow as tf 
from tensorflow import keras
from note import get_notes, get_int_notes, get_note_strings, get_notes_chords_list
from predict import get_new_series
from numpy import array
from music21 import stream
import argparse

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
train_output_file = open(args.model,'rb') if args.model else open('models/elementsmaster', 'rb')
output_file_path = args.output if args.output else 'results/output.mid'
model = keras.models.load_model("models/model_Master")

notes = get_notes(input_predict)
train_output = pickle.load(train_output_file)
pitchnames = train_output['pitchnames']
x_input = array(get_int_notes(pitchnames, notes))
x_input = x_input[0:train_output['groups_size']]


train_output_file.close()
predictions = []
int_to_note = dict((number, note) for number, note in enumerate(pitchnames))
new_series = get_new_series(train_output['groups_size'], x_input, model, len(pitchnames))
note_strings = get_note_strings(int_to_note, new_series)
output_notes = get_notes_chords_list(note_strings, 0.5)

midi_stream = stream.Stream(output_notes)
midi_stream.write('midi', fp=output_file_path)
