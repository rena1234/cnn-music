from typing import List, Dict, Union
from music21 import note, chord
from music21.note import Note
from music21.chord import Chord
import glob

from music21 import converter, instrument


def get_notes_info(data_path: str):
    """
    :param data_path: path to midis directory 

    :return: List of note strings 
    """
    notes_info = {'notes': [], 'offsets': [] };
    for file in glob.glob(data_path):
        try:
            midi = converter.parse(file)
        except:
            continue
        notes_to_parse = None
        parts = instrument.partitionByInstrument(midi)
        if parts:
            notes_to_parse = parts.parts[0].recurse()
        else:
            notes_to_parse = midi.flat.notes
        for element in notes_to_parse:
            if isinstance(element, note.Note):
                notes_info['notes'].append(str(element.pitch))
                notes_info['offsets'].append(element.offset)
            elif isinstance(element, chord.Chord):
                notes_info['notes'].append(".".join(str(n) for n in element.normalOrder))
                notes_info['offsets'].append(element.offset)
    return notes_info

def get_pitchnames(notes: List[str]) -> List[str]:
    """
    :param notes: List of note strings 

    :return: Set of sorted notes  
    """
    return sorted(set(item for item in notes))


def get_int_notes(pitchnames: List[str], notes: List[str]) -> List[int]:
    """
    :param pitchnames: Set of sorted note names 
    :param notes: Sequence of note strings 

    :return: List of integers representing the notes  
    """
    note_to_int = dict((note, number) for number, note in enumerate(pitchnames))
    int_notes = []
    for char in notes:
        if char in note_to_int.keys():
            int_notes.append(note_to_int[char])
        else:
            pitchnames_with_note = pitchnames[:]
            pitchnames_with_note.append(char)
            pitchnames_with_note.sort()
            index_new_element = pitchnames_with_note.index(char)
            set_size = len(pitchnames)
            int_notes.append(index_new_element if index_new_element < set_size else set_size - 1)

    return int_notes

def get_notes_chords_list(
    note_strings: List[str], offsets 
) -> List[Union[Chord, Note]]:
    """
    :param note_strings: List of note strings 
    :param offset_between: offset between notes and chords 

    :return: List of music21 Chords and notes 
    """
    offset = 0
    output = []

    for pattern, offset in zip(note_strings, offsets):
        print(offset)
        if ("." in pattern) or pattern.isdigit():
            notes_in_chord = pattern.split(".")
            notes = []
            for current_note in notes_in_chord:
                new_note = note.Note(int(current_note))
                new_note.storedInstrument = instrument.Piano()
                notes.append(new_note)
            new_chord = chord.Chord(notes)
            new_chord.offset = offset
            output.append(new_chord)

        else:
            new_chord = note.Note(pattern)
            new_chord.offset = offset
            new_chord.storedInstrument = instrument.Piano()
            output.append(new_chord)

    return output


def get_note_strings(int_to_note: Dict[int, str], series: List[int]) -> List[str]:
    """
    :param int_to_note: Dict to translate integers to note strings 
    :param series: Number series representing notes

    :return: List of note strings 
    """
    return [int_to_note[number] for number in series]
