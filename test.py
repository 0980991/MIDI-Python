from midiutil import MIDIFile
import random as r
#          1    2   3   4   5   6   7   8   9  10  11  12  13  14  15  # Scale intervals
degrees = [60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79, 81, 83, 84] # C Major / 2 Octaves

root = degrees[0]

middle_triads = [2, 3, 4] # Chord numbers (converted from roman numerals) that fit best in between 1st and last chord

start_end_triads = [1, 5, 6] # Chords that fit best first and/or last

MyMidi = MIDIFile(1)

time = 0
for i in range(1):

    progression = []
    for chord in range(4):
        if chord == 0:   # First chord in progression
            progression.append(1)
        elif chord == 3: # Last chord in progression
            progression.append(r.choice(start_end_triads))
        else:
            random_triad = r.choice(middle_triads)
            while random_triad == progression[chord-1]:
                random_triad = r.choice(middle_triads)
            progression.append(random_triad)

    chordstr = ''
    for chord in progression:
        chordstr += f', {chord}'
    print(chordstr[2:])

    for chord in progression:
        triad_pitches = None
        ### Determine and set first note in triad
        for chord_option in range(6):
            if chord == chord_option + 1:
                triad_pitches = [degrees[chord_option]]

                triad_pitches.append(degrees[chord_option + 2])
                triad_pitches.append(degrees[chord_option + 4])

        print(triad_pitches)

        for pitch in triad_pitches:
            print(str(pitch) + ' note added.')
            MyMidi.addNote(0, 1, pitch, time, 4, 100)
        time += 4
        print(str(chord) + ' chord added')

with open(f'chord_prog.mid', "wb") as outputfile:
    MyMidi.writeFile(outputfile)