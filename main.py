from midiutil import MIDIFile
import random as r
class BeatMaker:
    def __init__(self):
        #####DEFAULT VALUES########
        # Range of notes where 60 = C5
        self.degrees  = [60, 62, 63, 65, 67, 68, 70, 72] # C minor
        # Track to which notes are added (Piano roll???)
        self.track    = 0
        # MIDI self.channel nr
        self.channel  = 1
        # Time at which the note is played in a bar
        self.time     = 0
        # Length of note
        self.duration = 1
        # BPM
        self.tempo    = 140
        # Volume 0-127
        self.volume   = 100
        # Amount of bars per song
        self.amt_bars = 4
        # Amount of beats per bar
        self.beats    = 4
        # Instance of Midi object
        self.MyMIDI   = MIDIFile(1)
        # List of all notes in order
        self.notes = []

    def addToMIDI(self):
        # track = [[[track, channel, pitch, time, duration, volume], [1], [2], [3]], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
        
        for bar_nr in range(self.amt_bars):
            for note_nr in range(bar_nr): # Time = note number
                self.MyMIDI.addNote(self.track, self.channel, self.pitch, note_nr, self.duration, self.volume)

    def generateDegrees(self, rootdegree, amt, scale):
        if scale == 'major':
            intervals = [2, 2, 1, 2, 2, 2, 1] # Whole, whole, half, whole, whole, whole, half steps.
        elif scale == 'minor':
            intervals = [2, 1, 2, 2, 1, 2, 2] # Whole, half, whole, whole, half, whole, whole steps.
        else:
            print('This scale has not been implemented')
            return

        degrees = [rootdegree] * amt # sets all values to the rootnote, but all elements except for [0] will be overwritten.
        # Fills the degree list with notes according to the selected interval 'scheme'
        for i in range(1, amt):
            degrees[i] = degrees[i-1] + intervals[(i-1)%len(intervals)]
        self.degrees = degrees

    def generateMelody(self):
        bassdegrees = [self.degrees[0] - 12, self.degrees[4] - 12, self.degrees[3] - 12, self.degrees[5] - 12] # (Semi) Hardcoded bass notes (will adjust to major/minor)
        bassnote = 0
        for bars in range(self.amt_bars):
            self.MyMIDI.addNote(self.track, self.channel, bassdegrees[bassnote % 4], self.time, 4, self.volume)
            bassnote += 1
            self.generateBar()

    def generateBar(self):
        for beat in range(self.beats):
            self.pitch = r.choice(self.degrees)
            self.MyMIDI.addNote(self.track, self.channel, self.pitch, self.time, self.duration, self.volume)

            self.time = self.time + 1

    def generateTriads(self):
        middle_triads = [2, 3, 4] # Chord numbers (converted from roman numerals) that fit best in between 1st and last chord

        start_end_triads = [5, 6] # Chords that fit best first and/or last

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
                        triad_pitches = [self.degrees[chord_option]]

                        triad_pitches.append(self.degrees[chord_option + 2])
                        triad_pitches.append(self.degrees[chord_option + 4])

                for pitch in triad_pitches:
                    self.MyMIDI.addNote(0, 1, pitch - 12, time, 4, 100) # -12 sets it 1 octave lower than the melody
                time += 4

    def setAmountBars(self, amt):
        self.amt_bars = amt

    def setBeatsPerBar(self, amt):
        self.beats = amt

    def exportToMidi(self, filename):
        with open(f'{filename}.mid', "wb") as outputfile:
             self.MyMIDI.writeFile(outputfile)


if __name__ == "__main__":
    bm = BeatMaker()
    bm.generateDegrees(57, 14, 'major')
    bm.generateTriads()
    bm.generateMelody()
    bm.exportToMidi('a-major-triads-and-melody')