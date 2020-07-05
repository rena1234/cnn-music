import pickle
import argparse, sys
#from note import get_notes, get_pitchnames, get_int_notes
#from model import get_model_inputs, get_model
import note 
import model 
import json
from numpy import array
import argparse

input_parser = argparse.ArgumentParser('Trains a model')
input_parser.add_argument('-c','--config',
        metavar='config.json',
        type=str,
        help='path to config json; configs/config.json assumed if not specifyed'
        )
input_parser.add_argument('-o','--output',
        metavar='output',
        type=str,
        help='path to output; models/model assumed if not specifyed'
        )
input_parser.add_argument('-mp','--midipath',
        metavar='\*.mid',
        type=str,
        help='path to mid, you can use \*.mid for all midis on directory; dataset/*.mid assumed if not specifyed'
        )
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
output_file = open(outputpath,'wb')
pickle.dump(train_output,output_file)
output_file.close()
