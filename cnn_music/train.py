from numpy import array
from numpy import hstack
import numpy
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Dropout
import note
from model import get_model_inputs
from model import get_model
from music21 import stream
import pickle
import argparse, sys
import json

input_parser = argparse.ArgumentParser('Trains a model')
input_parser.add_argument('-c','--config',
        metavar='config.json',
        type=str,
        help='path to config json; configs/config.json assumed if not specifyed'
        )
input_parser.add_argument('-mp','--midipath',
        metavar='\*.mid',
        type=str,
        help='path to mid, you can use \*.mid for all midis on directory; dataset/*.mid assumed if not specifyed'
        )
args = input_parser.parse_args()
midipath = args.midipath if args.midipath else 'dataset/*.mid'
configpath = args.config if args.config else 'configs/config.json'

data = note.get_notes_info(midipath);
pitchnames = note.get_pitchnames(data['notes']);
in_seq1 = array(note.get_int_notes(pitchnames, data['notes']))
in_seq2 = array((data['offsets']))
parameters = json.load(open(configpath));

X, y = get_model_inputs(in_seq1, in_seq2, parameters['groups_size'])
n_features = X.shape[2]

model = get_model(X, y, parameters);
model.save('models/modelOffSet')
output_file = open("models/modelOffSett",'wb')
train_output = {
        'pitchnames': pitchnames,
        'groups_size': parameters['groups_size'],
        'n_features': n_features
        }
pickle.dump(train_output,output_file)
output_file.close()
