from midiutil import MIDIFile
import random as r
class BeatMaker:
    def __init__(self):
        #####DEFAULT VALUES########
        # Range of notes where 60 = C5
        self.degrees = [60, 62, 63, 65, 67, 68, 70, 72] # C minor
        # Track to which notes are added (Piano roll???)
        self.track   = 0
        # MIDI self.channel nr
        self.channel = 1
        # Time at which the note is played in a bar
        self.time    = 0
        # Length of note
        self.duration = 1
        # BPM
        self.tempo = 140
        # Volume 0-127
        self.volume = 100
        # Amount of beats per bar
        self.beats = 4
        # Amount of bars per song
        self.amtbars = 64
        # Instance of Midi object
        self.MyMIDI = MIDIFile(1)

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
        for bars in range(self.amtbars):
            self.MyMIDI.addNote(self.track, self.channel, bassdegrees[bassnote % 4], self.time, 4, self.volume)
            bassnote += 1
            self.generateBar()

    def generateBar(self):
        for beat in range(self.beats):
            self.pitch = r.choice(self.degrees)
            self.MyMIDI.addNote(self.track, self.channel, self.pitch, self.time, self.duration, self.volume)

            self.time = self.time + 1

    def setAmountBars(self, amt):
        self.amtbars = amt

    def setBeatsPerBar(self, amt):
        self.beats = amt

    def exportToMidi(self, filename):
        with open(f'{filename}.mid', "wb") as outputfile:
            self.MyMIDI.writeFile(outputfile)


if __name__ == "__main__":
    bm = BeatMaker()
    bm.generateDegrees(57, 14, 'major')
    bm.generateMelody()
    bm.exportToMidi('a-major-melody')