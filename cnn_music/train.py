import pickle
import argparse, sys
#from note import get_notes, get_pitchnames, get_int_notes
#from model import get_model_inputs, get_model
import note 
import model 
import json
from numpy import array
import argparse
from datetime import datetime

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
input_parser.add_argument('-t','--type',
        metavar='offset',
        type=str,
        help='trains offsets instead of notes when set to offset'
        )
args = input_parser.parse_args()
midipath = args.midipath if args.midipath else 'dataset/*.mid'
offset = True if (args.type and args.type == 'offset')  else False
configpath = args.config if args.config else 'configs/config.json'
outputpath = args.output if args.output else 'models/model_blues' if not offset else 'models_offset/model_blues'

# notes = note.get_notes(midipath);
data = note.get_notes_info(midipath);
parameters = json.load(open(configpath));
sequence_length = parameters['groups_size']
data_list = None
notes = data['notes']

if not offset:
    pitchnames = note.get_pitchnames(notes);
    int_notes = note.get_int_notes(pitchnames, notes)
    data_list = int_notes
else:
    data_list = data['offsets']

x, y = model.get_model_inputs(data_list, sequence_length)
x = array(x)
x = x.reshape((x.shape[0]), x.shape[1], 1)
y = array(y)
print(datetime.now().time())
model, history = model.get_model(x, y, parameters)
print(datetime.now().time())
model.save(outputpath)

if not offset:
    output_file = open(outputpath + '_notes_info','wb')
    train_output = {
            'pitchnames': pitchnames,
            'groups_size': sequence_length,
            }

    pickle.dump(train_output,output_file)
    output_file.close()
else:
    output_file = open(outputpath + '_info','wb')
    train_output = {
            
            'groups_size': sequence_length,
            }

    pickle.dump(train_output,output_file)
    output_file.close()