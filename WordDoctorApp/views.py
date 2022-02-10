from django.shortcuts import render
from .forms import AnagramsForm, WordscapeForm

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

            # oxford will have the entire applicable dictionary of related words within it
            oxford = Trie()

            # t will be the Trie to which we add words which are anagrams
            t = Trie()

            word_dict = dict.fromkeys([num for num in range(SCRABBLE_START + 1, len(word_to_anagram) + 1, 1)])

            for key in word_dict.keys():
                word_dict[key] = []

            # going through scrabble dictionary to use this as the basis for finding anagrams
            with open("words.txt") as file:
                word_list = file.readlines()

            # stripping white space and adding words to Trie, and dictionary;
            # dictionary used to reduce the search space of any anagram look up 
            # for a certain permutation of chars in our choice word;
            # there is a build function based on a list of words but I wanted to
            # strip each word and allow for words that are too large to be
            # omitted from the Trie
            for word in word_list:
                word = word.strip()

                # only allowing words that are longer than 2 chars and shorter than
                # the word we're trying to anagram
                if len(word) <= len(word_to_anagram) and len(word) > SCRABBLE_START:
                    word_dict[len(word)].append(word)
                    oxford.add(word)
            
            # helper function allowing us to find permutations;
            # python is all pass-by-reference so this works fine
            find_anagram_words(oxford, t, sorted(word_to_anagram), "")

            anagrams = []

            for key in word_dict.keys():
                for word in word_dict[key]:
                    if t.contains(word):
                        anagrams.append(word)

            context['anagrams_results'] = anagrams
            context['anagrams_letters'] = word_to_anagram

        else:
            form = AnagramsForm(request.POST or None)

    return render(request, 'anagrams.html', context)

def boggle(request):
    context = {}
    return render(request, 'boggle.html', context)

def wordscape(request):
    context = {}
    form = WordscapeForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            wordscape_chars = form.cleaned_data.get('wordscape_letters').strip().lower()
            word_size = form.cleaned_data.get('wordscape_length')

            # oxford will have the entire applicable dictionary of related words within it
            oxford = Trie()

            # t will be the Trie to which we add words which are anagrams
            t = Trie()

            # word_search_space will be all applicable words of a certain size 
            word_search_space = []

            with open("words.txt") as file:
                word_list = file.readlines()

            for word in word_list:
                word = word.strip()

                # only allowing words that are longer than 2 chars and shorter than
                # the word we're trying to anagram
                if len(word) == word_size:                  # FIXME: DOESN'T WORK WITHOUT OPTIONAL WORD LENGTH
                    word_search_space.append(word)
                    oxford.add(word)
            
            find_anagram_words(oxford, t, sorted(wordscape_chars), "")

            wordscapes_solutions = []

            for word in word_search_space:
                if t.contains(word):
                    wordscapes_solutions.append(word)
            
            context['wordscape_results'] = wordscapes_solutions
            context['wordscape_letters'] = wordscape_chars
    
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