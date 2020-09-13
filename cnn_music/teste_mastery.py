# multivariate output 1d cnn example
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

# split a multivariate sequence into samples
def split_sequences(sequences, n_steps):
    X, y = list(), list()
    for i in range(len(sequences)):
        # find the end of this pattern
        end_ix = i + n_steps
        # check if we are beyond the dataset
        if end_ix > len(sequences)-1:
            break
        # gather input and output parts of the pattern
        seq_x, seq_y = sequences[i:end_ix, :], sequences[end_ix, :]
        X.append(seq_x)
        y.append(seq_y)
    return array(X), array(y)

# define input sequence

midipath = 'dataset/*.mid'
data = note.get_notes_info(midipath);
pitchnames = note.get_pitchnames(data['notes']);
in_seq1 = array(note.get_int_notes(pitchnames, data['notes']))
in_seq2 = array((data['offsets']))

"""
in_seq1 = array([4, 10, 19, 18, 25, 31, 18, 34, 4])
in_seq2 = array([10.75, 11.25, 11.75, 14, 14.25, 15.33, 19.25, 19.5, 20.25])
"""

"""
in_seq1 = array(int_notes)
in_seq2 = array(offsets)
"""
# convert to [rows, columns] structure
in_seq1 = in_seq1.reshape((len(in_seq1), 1))
in_seq2 = in_seq2.reshape((len(in_seq2), 1))
# horizontally stack columns
dataset = hstack((in_seq1, in_seq2))
# choose a number of time steps
#n_steps = 3
n_steps = 100
# convert into input/output
X, y = split_sequences(dataset, n_steps)
# the dataset knows the number of features, e.g. 2
print('X----------------------------------------')
print(X);
n_features = X.shape[2]
# define model
model = Sequential()
model.add(Conv1D(filters=64, kernel_size=2, activation='relu', input_shape=(n_steps, n_features)))
model.add(MaxPooling1D(pool_size=2))
model.add(Flatten())
model.add(Dense(50, activation='relu'))
model.add(Dense(n_features))
model.compile(optimizer='adam', loss='mse')
# fit model
model.fit(X.astype(numpy.float32), y.astype(numpy.float32), epochs=3000, verbose=0)
# demonstrate prediction
#x_input = array([[34, 24.33, 58.33], [4, 24.75 , 28.75], [4, 27.33, 31.33]])

input_predict = 'ArtPepper_BluesForBlanche_FINAL.mid'
data_input_predict = note.get_notes_info(input_predict);
x_input_notes = note.get_int_notes(pitchnames, data_input_predict['notes'])
x_input_ofsets = data_input_predict['offsets']
x_input = [[x_input_notes[i], x_input_ofsets[i]] for i in range(100)]


#x_input = get_prediction_input(x_input_notes, x_input_ofsets, sequence_length)
#x_input = x_input[0:100]

new_series = x_input;
x_input = array(x_input);
x_input = x_input.reshape((1, n_steps, n_features))
last_offset = 0
for i in range(100):
    """
    offset_diff = -1
    while offset_diff < 0:
        print('loop')
        yhat = model.predict(x_input.astype(numpy.float32), verbose=0)
        offset_diff = yhat[0][1] - last_offset
        print(yhat)
    """
    yhat = model.predict(x_input.astype(numpy.float32), verbose=0)
    offset_diff = yhat[0][1] - last_offset
    if(offset_diff < 0):
        yhat[0][1] = last_offset + 0.5
    
    #print('out of the black');
    last_offset = yhat[0][1]
    new_series = new_series[1:100]
    new_series.append(yhat[0])
    x_input = new_series
    x_input = array(x_input);
    x_input = x_input.reshape((1, n_steps, n_features))

"""
print('NEW SERIEEEES-----------------------')
print(new_series)
"""

"""
    ROUND CAUSES THE NOTE NOT FOUND BUG
"""

int_notes = [ round(prediction[0]) if prediction[0] >= 0 else 0 for prediction in new_series ]
int_notes = [ n if n < len(pitchnames) else len(pitchnames) -1 for n in int_notes]

offsets = [ prediction[1] for prediction in new_series ]
#int_notes = int_notes.astype(int)
print('int_notes--------------------')
print(int_notes)
int_to_note = dict((number, note) for number, note in enumerate(pitchnames))
notes_strs = note.get_note_strings(int_to_note, int_notes)
notes_list = note.get_notes_chords_list_offset(notes_strs, offsets)

midi_stream = stream.Stream(notes_list)
output_file_path = 'results/output_mastey.mid'
midi_stream.write('midi', fp=output_file_path)
