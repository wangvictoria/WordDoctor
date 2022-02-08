from django.shortcuts import render
from .forms import AnagramsForm

from gettext import npgettext
import multiprocessing as mp
from multiprocessing.dummy import Process, Manager
from re import I
from python_datastructures import Trie
import numpy as np
import itertools as it

SCRABBLE_START = 2
SCRABBLE_END = 15
WORDLE_LEN = 5
ALPHABET_START = 1
ALPHABET_END = 26
BOGGLE_SIDE_LEN = 4
BOGGLE_WORD_MAX = 4
#PATH = "/Users/shaneausmus/Desktop/Vandy Course Materials/Spring 2022/CS 4279/WordDoctor"
SCRABBLE_LETTER_SCORES = {"A": 1, "E": 1, "I": 1, "O": 1, "U": 1, "L": 1, "N": 1,
                        "S": 1, "T": 1, "R": 1, "D": 2, "G": 2, "B": 3, "C": 3,
                        "M": 3, "P": 3, "F": 4, "H": 4, "V": 4, "W": 4, "Y": 4,
                        "K": 5, "J": 8, "X": 8, "Q": 10, "Z": 10} 

# Create your views here.

def index(request):
    """View function for home page of site."""

    context = {}

    return render(request, 'index.html', context)

def wordle(request):
    context = {}
    return render(request, 'wordle.html', context)

def scrabble(request):
    context = {}
    return render(request, 'scrabble.html', context)

def anagrams(request):
    context = {}
    form = AnagramsForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            word_to_anagram = form.cleaned_data.get('anagrams_letters')
            
            word_list = None

            # going through scrabble dictionary to use this as the basis for finding anagrams
            with open("ospd.txt") as file:
                word_list = file.readlines()

            # converting word_arr for ease of manipulation
            word_dict = dict.fromkeys([num for num in range(SCRABBLE_START, len(word_to_anagram) + 1, 1)])

            for key in word_dict.keys():
                word_dict[key] = []
            
            # stripping white space and adding words to Trie, and dictionary;
            # dictionary used to reduce the search space of any anagram look up 
            # for a certain permutation of chars in our choice word
            for word in word_list:
                word = word.strip()
                if len(word) <= len(word_to_anagram):
                    word_dict[len(word)].append(word)
            
            # finding what amounts to the powerset of the word's chars to
            # find out whether each combination of words counts as an actual
            # word in the OSPD
            word_to_anagram_combinations = []
            for i in range(SCRABBLE_START, len(word), 1):
                for combo in it.combinations(word_to_anagram.strip().lower(), i):
                    word_to_anagram_combinations.append("".join(combo))
            
            word_to_anagram_permutations = []

            for word in word_to_anagram_combinations:
                word_to_anagram_permutations += list(it.permutations(word))
            
            word_to_anagram_permutations_strings = []

            for word in word_to_anagram_permutations:
                word_to_anagram_permutations_strings.append("".join(word))

            # eliminating duplicates
            word_to_anagram_permutations_strings = list(set(word_to_anagram_permutations_strings))
            
            anagrams = []

            # checking to see if all anagrams combos are a valid word in the OSPD,
            # and therefore if it is a valid anagram
            for word in word_to_anagram_permutations_strings:
                if word in word_dict[len(word)]:
                    anagrams.append(word)

            anagrams = sorted(list(set(anagrams)), key=len)

            context['anagrams_results'] = anagrams

        else:
            form = AnagramsForm(request.POST or None)

    return render(request, 'anagrams.html', context)

def boggle(request):
    context = {}
    return render(request, 'boggle.html', context)

def wordscape(request):
    context = {}
    return render(request, 'wordscape.html', context)

def general(request):
    context = {}
    return render(request, 'general.html', context)


# HELPER METHODS
def find_anagram_words(oxford, t, word_to_anagram, text):
    for i in range(0, len(word_to_anagram), 1):
        text1 = text + word_to_anagram[i]
        if oxford.contains(text1) and not t.contains(text1):
            t.add(text1)
            text2 = word_to_anagram[0:i] + word_to_anagram[i + 1:]
            find_anagram_words(oxford, t, text2, text1)