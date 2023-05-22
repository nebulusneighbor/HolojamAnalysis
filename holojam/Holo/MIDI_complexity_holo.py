import os
import numpy as np
import zlib
from music21 import converter, note, chord

def lz_complexity(string):
    """Lempel-Ziv complexity of a string"""
    i, k, l = 0, 1, 1
    k_max = 1
    n = len(string)
    while True:
        if string[i:i+k] not in string[0:i+k]:
            if k > k_max:
                k_max = k
            if i+k<n:
                i = i+k
                k = 1
                l = l+1
            elif i+k>=n:
                l = l+1
                break
        elif string[i:i+k] in string[0:i+k] and string[i:i+k+1] not in string[0:i+k+1]:
            if i+k<n:
                i = i+k
                k = 1
                l = l+1
            elif i+k>=n:
                l = l+1
                break
        elif string[i:i+k] in string[0:i+k] and string[i:i+k+1] in string[0:i+k+1]:
            k = k+1
    return l

def analyze_midi(file_path):
    """Analyze a single midi file for unique notes"""
    midi = converter.parse(file_path)
    notes_to_parse = None
    try: # file has instrument parts
        s2 = instrument.partitionByInstrument(midi)
        notes_to_parse = s2.parts[0].recurse() 
    except: # file has notes in a flat structure
        notes_to_parse = midi.flat.notes

    pitch_sequence = ''
    for element in notes_to_parse:
        if isinstance(element, note.Note):
            pitch_sequence += str(element.pitch)
        elif isinstance(element, chord.Chord):
            pitch_sequence += ''.join(str(n) for n in element.normalOrder)
    
    complexity = lz_complexity(pitch_sequence)
    return complexity

print('debug 1')

midi_folder = 'C:/Users/torin/holojam/Holo'
midi_files = os.listdir(midi_folder)
complexities = [analyze_midi(os.path.join(midi_folder, f)) for f in midi_files if f.endswith('.mid') or f.endswith('.midi')]

mean_complexity = np.mean(complexities)
median_complexity = np.median(complexities)
std_dev = np.std(complexities)

print('debug 2')

print(f'Mean Complexity: {mean_complexity}')
print(f'Median Complexity: {median_complexity}')
print(f'Standard Deviation: {std_dev}')
