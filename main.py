from midiutil import MIDIFile


# Assuming that an octave is 12 degrees and '60' = C5
degrees = [60, 62, 63, 65, 67, 68, 70, 72] # C minor
# Track to which notes are added (Piano roll???)
track   = 0
# MIDI channel nr
channel = 1
# Time at which the note is played in a bar
time    = 1 
# Length of note
duration = 1
# BPM
tempo = 140
# Volume 0-127
volume = 100

MyMIDI = MIDIFile(1)
MyMIDI.addTempo(track, time, tempo)

for pitch in degrees:
    MyMIDI.addNote(track, channel, pitch, time, duration, volume)


with open("major-scale.mid", "wb") as outputfile:
    MyMIDI.writeFile(outputfile)