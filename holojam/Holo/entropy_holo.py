import os
import numpy as np
from music21 import converter, note, chord
from collections import Counter

def transition_entropy(midi_file):
    """Calculate transition entropy of a midi file"""
    midi = converter.parse(midi_file)
    notes_to_parse = midi.flat.notes

    note_transitions = []

    for i in range(len(notes_to_parse) - 1):
        note1 = notes_to_parse[i]
        note2 = notes_to_parse[i + 1]

        if isinstance(note1, note.Note):
            note1 = note1.pitch
        elif isinstance(note1, chord.Chord):
            note1 = '.'.join(str(n) for n in note1.pitches)

        if isinstance(note2, note.Note):
            note2 = note2.pitch
        elif isinstance(note2, chord.Chord):
            note2 = '.'.join(str(n) for n in note2.pitches)

        transition = (note1, note2)
        note_transitions.append(transition)

    transition_counts = Counter(note_transitions)
    total_transitions = sum(transition_counts.values())

    entropy = 0
    for count in transition_counts.values():
        probability = count / total_transitions
        entropy -= probability * np.log2(probability)

    return entropy

print('debug 1')

midi_folder = 'C:/Users/torin/holojam/Holo'
midi_files = os.listdir(midi_folder)
entropies = [transition_entropy(os.path.join(midi_folder, f)) for f in midi_files if f.endswith('.mid') or f.endswith('.midi')]

mean_entropy = np.mean(entropies)
median_entropy = np.median(entropies)
std_dev = np.std(entropies)

print('debug 2')

print(f'Mean Entropy: {mean_entropy}')
print(f'Median Entropy: {median_entropy}')
print(f'Standard Deviation: {std_dev}')
