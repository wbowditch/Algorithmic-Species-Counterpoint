import numpy
from music21 import *
from sklearn import svm
import random
import os


class state:
    def __init__(self, b1, b2, b3, s1, s2, pos):
        self.bassNotes = [b1,b2,b3]
        self.sopranoNotes = [s1,s2]
        self.counterpointIntervals = [interval.Interval(b1, s1), interval.Interval(b2, s2)]
        self.bassIntervals = [interval.Interval(b1, b2), interval.Interval(b2,b3)]
        self.sopranoIntervals = [interval.Interval(s1, s2)]
        self.position = pos #At what percent of the song will the note "s3" be played

    def getFeatures(self):
    	#return [self.bassNotes[0].pitchClass, self.bassNotes[1].pitchClass, self.bassNotes[2].pitchClass, self.sopranoNotes[0].pitchClass, self.sopranoNotes[1].pitchClass, self.counterpointIntervals[0].cents/50.0, self.counterpointIntervals[1].cents/50.0, (self.bassIntervals[0].cents/50), (self.bassIntervals[1].cents/50), (self.sopranoIntervals[0].cents/50), 10*self.position**3]
    	#return [self.counterpointIntervals[0].cents, self.counterpointIntervals[1].cents, (self.bassIntervals[0].cents), (self.bassIntervals[1].cents), (self.sopranoIntervals[0].cents), 10*self.position**3]
    	return [self.counterpointIntervals[0].semitones/32.0, self.counterpointIntervals[1].semitones/32.0, (self.bassIntervals[0].semitones/8.0), (self.bassIntervals[1].semitones/8.0), (self.sopranoIntervals[0].semitones/8.0), self.position]
    	#return [self.counterpointIntervals[0].semitones/1.0, self.counterpointIntervals[1].semitones/1.0, self.counterpointIntervals[2].semitones/1.0, (self.bassIntervals[0].semitones/1.0), (self.bassIntervals[1].semitones/1.0), (self.bassIntervals[2].semitones), (self.sopranoIntervals[0].semitones), self.sopranoIntervals[1].semitones, self.position]
    	#return [self.counterpointIntervals[0].semitones/1.0, self.counterpointIntervals[1].semitones/1.0, self.position]
    	#return [self.position]

    #NOTE: not used in current version
    def getLegalMoves(self): 
    	return [interval.transposeNote(self.sopranoNotes[1], 'M6'), 
    	interval.transposeNote(self.sopranoNotes[1], 'm6'), 
    	interval.transposeNote(self.sopranoNotes[1], 'P5'), 
    	interval.transposeNote(self.sopranoNotes[1], 'P4'), 
    	interval.transposeNote(self.sopranoNotes[1], 'M3'), 
    	interval.transposeNote(self.sopranoNotes[1], 'm3'), 
    	interval.transposeNote(self.sopranoNotes[1], 'M2'), 
    	interval.transposeNote(self.sopranoNotes[1], 'm2'), 
    	interval.transposeNote(self.sopranoNotes[1], 'P1'), 
    	interval.transposeNote(self.sopranoNotes[1], 'm-2'),
    	interval.transposeNote(self.sopranoNotes[1], 'M-2'), 
    	interval.transposeNote(self.sopranoNotes[1], 'm-3'), 
    	interval.transposeNote(self.sopranoNotes[1], 'M-3'), 
    	interval.transposeNote(self.sopranoNotes[1], 'P-4'), 
    	interval.transposeNote(self.sopranoNotes[1], 'P-5'), 
    	interval.transposeNote(self.sopranoNotes[1], 'm-6'), 
    	interval.transposeNote(self.sopranoNotes[1], 'M-6')]



data = []
targets = []

#Reading in the training data.
for file in os.listdir("training-data/fifths"):
	if file.endswith(".xml"):
		name= "training-data/fifths/"+file
		score = converter.parse(name)

		sopranoMeasures = score.parts[0].getElementsByClass("Measure").flat
		sopranoNotes = sopranoMeasures.getElementsByClass("Note")

		bassMeasures = score.parts[1].getElementsByClass("Measure").flat
		bassNotes = bassMeasures.getElementsByClass("Note")

		trainingcp = alpha.counterpoint.species.ModalCounterpoint(stream1 = bassNotes, stream2 = sopranoNotes)
		print "Number of Bad Harmonies in Training Data: ", trainingcp.countBadHarmonies(trainingcp.stream1, trainingcp.stream2)
		print "Accuracy: ", 100-(trainingcp.countBadHarmonies(trainingcp.stream1, trainingcp.stream2)/(1.0*len(bassNotes))*100.0), "%"

		stateSpace = []
		for i in range (2, len(sopranoNotes)):
			stateSpace=stateSpace+[state(bassNotes[i-2], bassNotes[i-1], bassNotes[i], sopranoNotes[i-2], sopranoNotes[i-1], (1.0*i)/len(bassNotes))]
			#print "GENERIC INTERVAL", interval.Interval(sopranoNotes[i-1], sopranoNotes[i]).directedName[1:]
			#targets = targets+[interval.Interval(sopranoNotes[i-1], sopranoNotes[i]).directedName[1:]]
			targets = targets+[interval.Interval(bassNotes[i], sopranoNotes[i]).directedName[1:]]
			#print "Adding", interval.Interval(bassNotes[i], sopranoNotes[i]).directedName[1:]


		for s in stateSpace:
			data = data+[s.getFeatures()]



#Fitting the Model
clf = svm.SVC(C=10000)
clf.fit(data,targets)
#coefs=clf.coef_
#print "CLASSES", clf.classes_
#print "COEFS", clf.coef_
"""
print "0",clf.predict([coefs[0]]),"\n"
print "1",clf.predict([coefs[1]]),"\n"
print "2",clf.predict([coefs[2]]),"\n"
print "3",clf.predict([coefs[3]]),"\n"
print "4",clf.predict([coefs[4]]),"\n"
print "5",clf.predict([coefs[5]]),"\n"
print "6",clf.predict([coefs[6]]),"\n"
print "7",clf.predict([coefs[7]]),"\n"
print "8",clf.predict([coefs[8]]),"\n"
print "9",clf.predict([coefs[9]]),"\n"
print "10",clf.predict([coefs[10]]),"\n"
print "11",clf.predict([coefs[11]]),"\n"
print "12",clf.predict([coefs[12]]),"\n"
print "13",clf.predict([coefs[13]]),"\n"
print "14",clf.predict([coefs[14]]),"\n"
print "15",clf.predict([coefs[15]]),"\n"
print "16",clf.predict([coefs[16]]),"\n"
print "17",clf.predict([coefs[17]]),"\n"
print "18",clf.predict([coefs[18]]),"\n"
"""

#What key we are working in
key = key.KeySignature(0)

#Reading in the cantus firmus
cf_score = converter.parse('/Users/Champ/Desktop/AI/basslines/cf008-32bar.xml')

#Getting the cantus firmus' notes (the bassline)
cf_measures = cf_score[2].getElementsByClass("Measure").flat
cf_notes = cf_measures.getElementsByClass("Note")

#Creating the melody
melody=[]

#Randomly generating the first note

possibleFirstNotes=[note.Note('G4', quarterLength=4),note.Note('C5', quarterLength=4),note.Note('E5', quarterLength=4)]
melody.append(possibleFirstNotes[random.randint(0,2)])

#Randomly generating the second note
legal_moves = ['M3', 'm3', 'M2', 'm2', 'P1', 'm-2', 'M-2', 'm-3', 'M-3']
second_note = melody[0].transpose(interval.Interval(legal_moves[random.randint(0,len(legal_moves)-1)]))
if key.accidentalByStep(second_note.step) != second_note.pitch.accidental:
	second_note.pitch.accidental = key.accidentalByStep(second_note.step)


#Making sure the second note follows the counterpoint rules i.e. no 2nds, 4ths, or 7ths against the bass

while(interval.Interval(cf_notes[1], second_note).simpleName[-1]=='2' or interval.Interval(cf_notes[1], second_note).simpleName[-1]=='4' or interval.Interval(cf_notes[1], second_note).simpleName[-1]=='7'):
	second_note = melody[0].transpose(interval.Interval(legal_moves[random.randint(0,len(legal_moves)-1)]))
	if key.accidentalByStep(second_note.step) != second_note.pitch.accidental:
		second_note.pitch.accidental = key.accidentalByStep(second_note.step)

melody.append(second_note)


#Adding the rest of the notes, one by one
for j in range (2, len(cf_notes)):
	current_state = state(cf_notes[j-2], cf_notes[j-1], cf_notes[j], melody[j-2], melody[j-1], (1.0*j)/len(cf_notes))
	next_interval = clf.predict([current_state.getFeatures()])[0]
	predicted = next_interval
	

	if next_interval in ['1','4','5','8','11','12','15','18','19','22','25']:
		next_interval='P'+next_interval
	else:
		next_interval='M'+next_interval

	print current_state.getFeatures()

	weightmatrix = []
	#for i in clf.coef_:
	#	weightmatrix.append(numpy.dot(current_state.getFeatures(),i))

	#print clf.classes_[weightmatrix.index(max(weightmatrix))]==predicted


	next_note = cf_notes[j].transpose(interval.Interval(next_interval))

	#make sure the next note fits in the key
	if key.accidentalByStep(next_note.step) != next_note.pitch.accidental:
		next_note.pitch.accidental = key.accidentalByStep(next_note.step)

	#append it to the melody
	melody.append(next_note)



#Preparation for output
melody_output = stream.Part(id='part 1')
melody_stream = stream.Stream() #used in finding counterpoint errors

bass_output = stream.Part(id='part 0')
bass_output.append(clef.BassClef())
bass_stream = stream.Stream() #used in finding counterpoint errors

current_measure = 0
for b in cf_notes:
	measure=stream.Measure(number=current_measure)
	measure.append(b)
	bass_output.append(measure)
	bass_stream.append(b)
	current_measure+=1

	

current_measure = 0
index = 0
for s in melody:
	s.addLyric(interval.Interval(cf_notes[index],s).simpleName)
	measure=stream.Measure(number=current_measure)
	measure.append(s)
	melody_output.append(measure)
	melody_stream.append(s)
	current_measure+=1
	index+=1


#Showing the result
output = stream.Score()
output.insert(0,melody_output)
output.insert(1,bass_output)
output.show()


#Accuracy check
cp = alpha.counterpoint.species.ModalCounterpoint(stream1 = bass_stream, stream2 = melody_stream)
print "Number of Bad Harmonies: ", cp.countBadHarmonies(cp.stream1, cp.stream2)
print "Accuracy: ", 100-(cp.countBadHarmonies(cp.stream1, cp.stream2)/(1.0*len(melody))*100.0), "%"

