from typing import Dict
from random import randint
import json

with open("alphabet.json", encoding='utf-8') as file:
    ALPHABET = json.load(file, object_hook=lambda x: {a: float(b) * 100 for a, b in x.items()})

with open("bigram.json") as file:
    BIGRAMS = json.load(file, object_hook=lambda x: {a: float(b) * 100 for a, b in x.items()})

with open("trigram.json", encoding='utf-8') as file:
    TRIGRAMS = json.load(file, object_hook=lambda x: {a: float(b) * 100 for a, b in x.items()})

with open("first_freq.json", encoding='utf-8') as file:
    FIRST = json.load(file, object_hook=lambda x: {a: float(b) * 100 for a, b in x.items()})

VOWELS = {"A", "Å", "Ä", "O", "Ö", "E", "I", "U", "Y"}


class Data:

    def __init__(self):
        self.frequency: Dict[str, int] = {}
        self.total = 0

        for letter, val in ALPHABET.items():
            self.total += val
            self.frequency[letter] = self.total

        self.curr_frequency = dict(self.frequency)

    def change_probability(self, word: str, length: int) -> None:

        if len(word) == 0:
            self.total = 0
            for letter, freq in FIRST.items():
                self.total += freq
                self.curr_frequency[letter] = self.total

            self.total = list(self.curr_frequency.values())[-1]
            return None

        self.curr_frequency = dict(self.frequency)
        self.total = 0

        vowel_bonus, cons_bonus, dup_bonus = 0, 0, 0

        # last letter is not a vowel so we increase probability for a vowel
        if not self.is_vowel(word[-1]):
            vowel_bonus += 10

        # greater chance for vowel at the end of the word
        if len(word) + 1 >= length:
            vowel_bonus += 25

        # greater chance for vowel when first letter is a consonant
        if len(word) == 1 and not self.is_vowel(word[0]):
            vowel_bonus += 50

        # too few vowels, tremendously increase chance for a vowel
        if len(word) > 2 and not self.is_vowel(word[-1]) and not self.is_vowel(word[-2]):
            vowel_bonus += 100000  # was 50
            if len(word) > 3 and not self.is_vowel(word[-3]):
                vowel_bonus *= 100

        if len(word) > 2 and self.is_vowel(word[-1]) and self.is_vowel(word[-2]):
            cons_bonus += 15

        # increases chance for letters that usually follow last picked letter
        for dup in BIGRAMS:
            dup_bonus = 70 if len(word) + 2 >= length else 40
            if dup[0] == word[-1]:
                self.curr_frequency[dup[1]] += int(dup_bonus * BIGRAMS[dup])

        # increases chance for letters that usually follow two last picked letter
        if len(word) >= 2:
            for trip in TRIGRAMS:
                trip_bonus = 70 if length >= 5 else 40
                if trip[0] == word[-2] and trip[1] == word[-1]:
                    self.curr_frequency[trip[2]] += int(trip_bonus * TRIGRAMS[trip])

        self.increase_probab(vowel_bonus, cons_bonus)

        self.recalculate()
        self.total = list(self.curr_frequency.values())[-1]

    def increase_probab(self, vowel: int, consonant: int) -> None:
        for letter in ALPHABET:
            multiplier = vowel if self.is_vowel(letter) else consonant
            self.curr_frequency[letter] += multiplier * 100

    def pick_letter(self) -> str:
        rand = randint(1, self.total)
        for letter, freq in self.curr_frequency.items():
            if rand <= freq:
                return letter

    def is_vowel(self, letter: str) -> bool:
        return letter in VOWELS

    def recalculate(self) -> None:
        key_list = list(self.curr_frequency.keys())
        freq_list = [next(iter(self.curr_frequency.values()))] + [self.curr_frequency[key_list[key_idx]] - self.frequency[key_list[key_idx - 1]]
                                                                  for key_idx in range(1, len(key_list))]
        for i, freq in enumerate(freq_list):
            self.total += freq
            self.curr_frequency[key_list[i]] = self.total

    def get_letter(self, length: int, word: str) -> str:
        self.change_probability(word, length)
        return self.pick_letter()
        
