#!/usr/bin/env python3

from string import ascii_uppercase

class Note:

    NOTE_COUNT = 7
    NUMBERS = dict(enumerate(ascii_uppercase[:NOTE_COUNT]))
    NOTES = {v: k for k, v in NUMBERS.items()}

    def __init__(self, note=None, number=None):
        if note is not None and note.upper() in self.NOTES:
            note = note.upper()
        elif number is not None and number in self.NUMBERS:
            note = self.NUMBERS[number]
        else:
            raise Exception("Not a valid note")
        self._note = note 

    def __repr__(self):
        return "Note({._note!r})".format(self)

    @property
    def number(self):
        return self.NOTES[self._note]

    @property
    def note(self):
        return self._note

    @note.setter
    def note(self, new_note):
        new_note = new_note.upper()
        if new_note not in self.NOTES:
            raise Exception("Not a valid note")
        self._note = new_note

    def __add__(self, other):
        try:
            num = other.number
        except AttributeError:
            num = other
        return Note(number=((self.number+num)%self.NOTE_COUNT))

    def __sub__(self, other):
        try:
            num = other.number
        except AttributeError:
            num = other
        return Note(number=((self.number-num)%self.NOTE_COUNT))
