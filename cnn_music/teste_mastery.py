from numpy import array
from numpy import hstack
import numpy
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Conv1D
from tensorflow.keras.layers import MaxPooling1D
import note
from music21 import stream
import pickle
from multiprocessing import Queue
import argparse, sys
import json

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

midipath = 'dataset/*.mid'
data = note.get_notes_info(midipath);
pitchnames = note.get_pitchnames(data['notes']);
in_seq1 = array(note.get_int_notes(pitchnames, data['notes']))
in_seq2 = array((data['offsets']))

print(len(data['offsets']))
print(len(data['notes']))
print('LEN 1---------')
print(len(in_seq1))
print('--------------')
print('LEN 2---------')
print(len(in_seq2))
print('--------------')

in_seq1 = in_seq1.reshape((len(in_seq1), 1))
in_seq2 = in_seq2.reshape((len(in_seq2), 1))
dataset = hstack((in_seq1, in_seq2))
n_steps = 100
X, y = split_sequences(dataset, n_steps)

n_features = X.shape[2]

model = Sequential()
model.add(Conv1D(filters=64, kernel_size=2, activation='relu', input_shape=(n_steps, n_features)))
model.add(MaxPooling1D(pool_size=2))
model.add(Flatten())
model.add(Dense(50, activation='relu'))
model.add(Dense(n_features))
model.compile(optimizer='adam', loss='mse')
model.fit(X.astype(numpy.float32), y.astype(numpy.float32), epochs=100, verbose=0)

model.save('models/modelOffSet')

input_predict = 'ArtPepper_BluesForBlanche_FINAL.mid'
data_input_predict = note.get_notes_info(input_predict);
x_input_notes = note.get_int_notes(pitchnames, data_input_predict['notes'])
x_input_ofsets = data_input_predict['offsets']
x_input = [[x_input_notes[i], x_input_ofsets[i]] for i in range(100)]

new_series = x_input;
x_input = array(x_input);
x_input = x_input.reshape((1, n_steps, n_features))
last_offset = 0
for i in range(100):
    yhat = model.predict(x_input.astype(numpy.float32), verbose=0)
    offset_diff = yhat[0][1] - last_offset
    if(offset_diff < 0):
        yhat[0][1] = last_offset + 0.5
    
    last_offset = yhat[0][1]
    new_series = new_series[1:100]
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

output_file = open("models/modelOffSettt",'wb')
train_output = {
        'pitchnames': pitchnames,
        'groups_size': 100,
        'n_features': n_features
        }
pickle.dump(train_output,output_file)
output_file.close()

midi_stream = stream.Stream(notes_list)
output_file_path = 'results/output_mastey.mid'
midi_stream.write('midi', fp=output_file_path)
