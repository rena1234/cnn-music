import pickle, sys, note, argparse
import tensorflow as tf 
from tensorflow import keras
from predict import get_new_series, get_new_series_offset
from numpy import array
from music21 import stream


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
train_output_file_note = open(args.model,'rb') if args.model else open('models/model_1_notes_info', 'rb')
model_note = keras.models.load_model("models/model_1")
train_output_file_offset = open(args.model,'rb') if args.model else open('models_offset/model_1_info', 'rb')
model_offset = keras.models.load_model("models_offset/model_1")
train_output_note = pickle.load(train_output_file_note)
train_output_offset = pickle.load(train_output_file_offset)

input_predict = args.midi if args.midi else 'inputs/1_input.mid'
output_file_path = args.output if args.output else 'results/model_1.mid'


data_input_predict = note.get_notes_info(input_predict);

pitchnames = train_output_note['pitchnames']
x_input_note = array(note.get_int_notes(pitchnames, data_input_predict['notes']))
x_input_note = x_input_note[0:train_output_note['groups_size']]


x_input_offset = array(data_input_predict['offsets'])
x_input_offset = x_input_offset[0:train_output_offset['groups_size']]



int_to_note = dict((number, note) for number, note in enumerate(pitchnames))
new_series_note = get_new_series(train_output_note['groups_size'], x_input_note, model_note, len(pitchnames))
note_strings = note.get_note_strings(int_to_note, new_series_note)

new_series_offset = get_new_series_offset(train_output_offset['groups_size'], x_input_offset, model_offset)

first_offset = new_series_offset[0]
offsets = [ prediction - first_offset  for prediction in new_series_offset ]

output_notes = note.get_notes_chords_list(note_strings, offsets)

midi_stream = stream.Stream(output_notes)
midi_stream.write('midi', fp=output_file_path)
       

train_output_file_note.close()
train_output_file_offset.close()