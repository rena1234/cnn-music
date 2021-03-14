import pickle, argparse, sys, json, note
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.layers import Conv1D, MaxPooling1D
from tensorflow.keras.layers import Dropout
from datetime import datetime
from music21 import stream
from numpy import hstack
from numpy import array
import numpy


def split_sequences(sequences, n_steps):
    X, y = list(), list()
    for i in range(len(sequences)):
        end_ix = i + n_steps
        if end_ix > len(sequences)-1:
            break
        seq_x, seq_y = sequences[i:end_ix, :], sequences[end_ix, :]
        X.append(seq_x)
        y.append(seq_y)
    return array(X), array(y)


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

print("get notes")
print(datetime.now().time())

data = note.get_notes_info(midipath);
pitchnames = note.get_pitchnames(data['notes']);
in_seq1 = array(note.get_int_notes(pitchnames, data['notes']))
in_seq2 = array((data['offsets']))
parameters = json.load(open(configpath));
n_steps = parameters['groups_size']

in_seq1 = in_seq1.reshape((len(in_seq1), 1))
in_seq2 = in_seq2.reshape((len(in_seq2), 1))
dataset = hstack((in_seq1, in_seq2))

X, y = split_sequences(dataset, n_steps)

n_features = X.shape[2]

print("Treinando")
print(datetime.now().time())

model = Sequential()
model.add(Conv1D(filters=parameters['filters'], kernel_size=parameters['kernel_size'], activation=parameters['activation'], input_shape=(n_steps, n_features)))
model.add(Conv1D(filters=parameters['filters2'], kernel_size=parameters['kernel_size'], activation=parameters['activation'], input_shape=(n_steps, n_features)))
model.add(MaxPooling1D(pool_size=parameters['pool_size']))

model.add(Dense(parameters['dense_units'], activation=parameters['activation']))

model.add(Conv1D(filters=parameters['filters'], kernel_size=parameters['kernel_size'], activation=parameters['activation'], input_shape=(n_steps, n_features)))
model.add(Conv1D(filters=parameters['filters2'], kernel_size=parameters['kernel_size'], activation=parameters['activation'], input_shape=(n_steps, n_features)))
model.add(MaxPooling1D(pool_size=parameters['pool_size']))

model.add(Dense(parameters['dense_units'], activation=parameters['activation']))

model.add(Conv1D(filters=parameters['filters'], kernel_size=parameters['kernel_size'], activation=parameters['activation'], input_shape=(n_steps, n_features)))
model.add(Conv1D(filters=parameters['filters2'], kernel_size=parameters['kernel_size'], activation=parameters['activation'], input_shape=(n_steps, n_features)))
model.add(MaxPooling1D(pool_size=parameters['pool_size']))


model.add(Flatten())
model.add(Dense(parameters['dense_units'], activation=parameters['activation']))
model.add(Dense(n_features))
model.compile(optimizer=parameters['optimizer'], loss=parameters['loss'])
model.fit(X.astype(numpy.float32), y.astype(numpy.float32), epochs=parameters['epochs'], verbose=parameters['verbose'])

model.save('models/modelOffSet')

print("fim treino")
print(datetime.now().time())

output_file = open("models/modelOffSett",'wb')
train_output = {
        'pitchnames': pitchnames,
        'groups_size': parameters['groups_size'],
        'n_features': n_features
        }
pickle.dump(train_output,output_file)
output_file.close()