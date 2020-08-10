from music21 import instrument, stream, note, chord, midi
from unittest import TestCase, main
from note import get_notes, get_pitchnames, get_int_notes, get_notes_chords_list, get_notes_info
from numpy import array
import pickle

class TestNote(TestCase):

    def test_get_notes_info(self):
        def get_default_note(note_char, offset):
            new_note = note.Note(note_char)
            new_note.offset = offset 
            new_note.storedInstrument = instrument.Piano()
            return new_note

        output_notes = [ 
                get_default_note('A3', 0),
                get_default_note('C4', 0.5)
                ]

        midi_stream = stream.Stream(output_notes)
        midi_stream.write('midi', fp='test_notes.mid')

        notes_info = get_notes_info('test_notes.mid')
        notes_info_tuple = (notes_info['notes'], notes_info['offsets'])
        self.assertEqual(notes_info_tuple, (['A3', 'C4'], [0, 0.5]))

    def test_get_notes(self):
        def get_default_note(note_char, offset):
            new_note = note.Note(note_char)
            new_note.offset = offset 
            new_note.storedInstrument = instrument.Piano()
            return new_note

        output_notes = [ 
                get_default_note('A3', 0),
                get_default_note('C4', 0.5)
        ]

        midi_stream = stream.Stream(output_notes)
        midi_stream.write('midi', fp='test_notes.mid')

        notes = get_notes('test_notes.mid')
        self.assertEqual(notes, ['A3', 'C4'])
    

    def test_get_pitchnames(self):
        notes = ['4.6', 'D3', 'D3']
        notes_univere = get_pitchnames(notes)
        self.assertEqual(notes_univere, ['4.6', 'D3'])

    def test_get_int_notes(self):
        notes = ['4.6', 'D3', 'D3']
        pitchnames = ['4.6', 'D3']
        converted_notes = get_int_notes(pitchnames, notes)
        self.assertEqual(converted_notes, [0, 1, 1])


    def test_get_notes_chords_list(self):
        note_pitchs = [str(e.pitch) for e in get_notes_chords_list(['A','B'], 1)]
        self.assertEqual(note_pitchs,['A','B'])

if __name__ == '__main__':
    main()


