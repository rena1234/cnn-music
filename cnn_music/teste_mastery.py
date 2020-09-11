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
out_seq = array([in_seq1[i]+in_seq2[i] for i in range(len(in_seq1))])
# convert to [rows, columns] structure
in_seq1 = in_seq1.reshape((len(in_seq1), 1))
in_seq2 = in_seq2.reshape((len(in_seq2), 1))
out_seq = out_seq.reshape((len(out_seq), 1))
# horizontally stack columns
dataset = hstack((in_seq1, in_seq2, out_seq))
# choose a number of time steps
#n_steps = 3
n_steps = 100
# convert into input/output
X, y = split_sequences(dataset, n_steps)
# the dataset knows the number of features, e.g. 2
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

input_predict = 'input.mid'
data_input_predict = note.get_notes_info(input_predict);
x_input_notes = get_int_notes(pitchnames, data_input_predict['notes'])
x_input_ofsets = data_input_predict['offsets']
x_input = [[x_input_notes[i], x_input_ofsets[i], x_input_notes[i] + x_input_ofsets[i]] for i in range(100)]


#x_input = get_prediction_input(x_input_notes, x_input_ofsets, sequence_length)
#x_input = x_input[0:100]

x_input = x_input.reshape((1, n_steps, n_features))
yhat = model.predict(x_input, verbose=0)
print(yhat)
