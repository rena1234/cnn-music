import argparse, sys
import note 
import model 
import json
from numpy import array
import argparse
from note import get_notes, get_int_notes, get_note_strings, get_notes_chords_list
from predict import get_new_series
from music21 import stream

input_parser = argparse.ArgumentParser('Trains a model')
input_parser.add_argument('-o','--output',
        metavar='output.mid',
        type=str,
        help='path to output; results/output.mid assumed if not specifyed'
        )
input_parser.add_argument('-md','--midi',
        metavar='input.mid',
        type=str,
        help='path to input midi; input.mid assumed if not specifyed'
        )
input_parser.add_argument('-c','--config',
        metavar='config.json',
        type=str,
        help='path to config json; configs/config.json assumed if not specifyed'
        )
"""
input_parser.add_argument('-o','--output',
        metavar='output',
        type=str,
        help='path to output; models/model assumed if not specifyed'
        )
        """
input_parser.add_argument('-mp','--midipath',
        metavar='\*.mid',
        type=str,
        help='path to mid, you can use \*.mid for all midis on directory; dataset/*.mid assumed if not specifyed'
        )
print('passou inputs')

args = input_parser.parse_args()
midipath = args.midipath if args.midipath else 'dataset/*.mid'
configpath = args.config if args.config else 'configs/config.json'
outputpath = args.output if args.output else 'models/model'

notes = note.get_notes(midipath);
pitchnames = note.get_pitchnames(notes);
int_notes = note.get_int_notes(pitchnames, notes)
parameters = json.load(open(configpath));
sequence_length = parameters['groups_size']
x, y = model.get_model_inputs(int_notes, sequence_length)
x = array(x)
x = x.reshape((x.shape[0]), x.shape[1], 1)
y = array(y)
model, history = model.get_model(x, y, parameters)
train_output = {
        'pitchnames': pitchnames,
        'model': model,
        'groups_size': sequence_length,
        'history': history
        }
"""
output_file = open(outputpath,'wb')
pickle.dump(train_output,output_file)
output_file.close()
"""
input_predict = args.midi if args.midi else 'input.mid'
output_file_path = args.output if args.output else 'results/output.mid'
notes = get_notes(input_predict)
pitchnames = train_output['pitchnames']
x_input = array(get_int_notes(pitchnames, notes))
x_input = x_input[0:train_output['groups_size']]
model = train_output['model']

#train_output_file.close()
predictions = []
int_to_note = dict((number, note) for number, note in enumerate(pitchnames))
new_series = get_new_series(train_output['groups_size'], x_input, model, len(pitchnames))
note_strings = get_note_strings(int_to_note, new_series)
output_notes = get_notes_chords_list(note_strings, 0.5)
midi_stream = stream.Stream(output_notes)
midi_stream.write('midi', fp=output_file_path)
