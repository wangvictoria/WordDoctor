from django.shortcuts import render
from django.contrib import messages
from .forms import AnagramsForm, WordscapeForm, WordleForm, BoggleForm, ScrabbleForm

# Test

from math import ceil
from trie_test import My_Trie
from timeit import repeat
import numpy as np
import itertools as it
import collections

BOGGLE_WORD_MAX = 16
BOGGLE_WORD_MIN = 2
SCRABBLE_START = 3
SCRABBLE_END = 8
WORDLE_LEN = 5
ALPHABET_START = 1
ALPHABET_END = 26
BOGGLE_SIDE_LEN = 4
#BOGGLE_WORD_MAX = 4
SCRABBLE_LETTER_SCORES = {"a": 1, "e": 1, "i": 1, "o": 1, "u": 1, "l": 1, "n": 1,
                        "s": 1, "t": 1, "r": 1, "d": 2, "g": 2, "b": 3, "c": 3,
                        "m": 3, "p": 3, "f": 4, "h": 4, "v": 4, "w": 4, "y": 4,
                        "k": 5, "j": 8, "x": 8, "q": 10, "z": 10} 

# Create your views here.

def index(request):
    """View function for home page of site."""

    context = {}

    return render(request, 'index.html', context)

def wordle(request):
    form = WordleForm(request.POST or None)
    context = {'form': form}
    if request.method == 'POST':
        if form.is_valid():
            form.save()

            # TODO: check to see if form is empty

            # populate char locations
            char_locations = []
            char_list = ['a', 'b', 'c', 'd', 'e', 'f']
            wordle_char_locations(char_locations, form, 'wordle_loc1')
            wordle_char_locations(char_locations, form, 'wordle_loc2')
            wordle_char_locations(char_locations, form, 'wordle_loc3')
            wordle_char_locations(char_locations, form, 'wordle_loc4')
            wordle_char_locations(char_locations, form, 'wordle_loc5')

            num_known_characters = 0
            for i in range(0, WORDLE_LEN, 1):
                if char_locations[i] != "_":
                    num_known_characters = num_known_characters + 1

            spaces_in_wordle_word = dict.fromkeys([num for num in range(1, WORDLE_LEN + 1, 1)])

            while(len(char_list) + num_known_characters > WORDLE_LEN):
                char_list = []
                spaces_in_wordle_word[1] = form.cleaned_data.get('wordle_loc6')
                spaces_in_wordle_word[2] = form.cleaned_data.get('wordle_loc7')
                spaces_in_wordle_word[3] = form.cleaned_data.get('wordle_loc8')
                spaces_in_wordle_word[4] = form.cleaned_data.get('wordle_loc9')
                spaces_in_wordle_word[5] = form.cleaned_data.get('wordle_loc10')
                for i in range(1, WORDLE_LEN + 1, 1):
                    if spaces_in_wordle_word[i] == None:
                        spaces_in_wordle_word[i] = ""
                    else:
                        spaces_in_wordle_word[i] = spaces_in_wordle_word[i].strip().lower()
                for j in range(len(spaces_in_wordle_word)):
                    char_list.extend(list(spaces_in_wordle_word[j+1]))
                char_list = list(set(char_list))
            

            check_for_invalid_letters = ""
            invalid_chars = ""
            if form.cleaned_data.get('wordle_invalid_letters') != None:
                invalid_chars = list(set(form.cleaned_data.get('wordle_invalid_letters').strip().lower()))


            if len(invalid_chars) == 0:
                check_for_invalid_letters = False

            with open("wordle.txt", "r") as file:
                word_list = file.readlines()

                # array holding all applicable words
                wordle_solutions = []

                for word in word_list:
                    valid = True
                    word = word.strip()
                    for j in range(0, WORDLE_LEN, 1):
                        if char_locations[j] != "_":
                            if word[j] != char_locations[j]:
                                valid = False
                                break
                        if word[j] in spaces_in_wordle_word[j + 1]:
                            valid = False
                            break
                    if valid:
                        if len(char_list) == 0:
                            wordle_solutions.append(word)
                        else:
                            for i in range(0, len(char_list), 1):
                                if char_list[i] not in word:
                                    break
                                if i == len(char_list) - 1:
                                    wordle_solutions.append(word)

            filtered_wordle_solutions = []

            if invalid_chars:
                for word in wordle_solutions:
                    for i in range(0, WORDLE_LEN, 1):
                        if word[i] in invalid_chars:
                            break
                        if i == WORDLE_LEN - 1:
                            filtered_wordle_solutions.append(word)

            if invalid_chars and filtered_wordle_solutions:
                context['filtered_wordle_solutions'] = filtered_wordle_solutions
            elif not invalid_chars and wordle_solutions:
                context['wordle_solutions'] = wordle_solutions
            else:
                context['wordle_no_solutions'] = 'There are no words with the requested letters.\n'


    return render(request, 'wordle.html', context)

def scrabble(request):
    form = ScrabbleForm(request.POST or None)
    context = {'form': form}
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            user_chars = form.cleaned_data.get('scrabble_letters').strip().lower()
            chars_on_board = form.cleaned_data.get('scrabble_open').strip().lower()

            context['scrabble_letters'] = user_chars
            context['chars_on_board'] = chars_on_board

            with open("ospd.txt", "r") as file:
                word_list = file.readlines()

            processed_list = [word.strip() for word in word_list if (len(word.strip()) >= SCRABBLE_START and len(word.strip()) <= SCRABBLE_END)]

            user_chars = list(user_chars.strip())
            chars_on_board = list(chars_on_board.strip())

            word_dict = {}

            scrabble_processing(word_dict, processed_list, chars_on_board, user_chars)

            keys_list = [key for key in word_dict.keys()]
            keys_list.sort(reverse=True)

            scrabble_list = []

            for i in range(SCRABBLE_START, len(user_chars) + 1, 1):
                if i in word_dict:
                    length_list = word_dict.get(i)
                    for j in length_list:
                        scrabble_list.append(j)

            # Ordering the dictionary by descending key
            ordered_word_dict = {}
            if (word_dict):
                ordered_word_dict = collections.OrderedDict(sorted(word_dict.items(), reverse=True))

            context['scrabble_ordered_dict'] = ordered_word_dict
            context['scrabble_words'] = scrabble_list
            context['scrabble_scores'] = keys_list
            context['scrabble_no_solutions'] = 'There are no words with the requested letters.\n'

            for key in keys_list:
                print(f'Scrabble solutions of score {key}:\n')
                print(*word_dict[key], sep=', ')
                print('\n')
    return render(request, 'scrabble.html', context)

def anagrams(request):
    form = AnagramsForm(request.POST or None)
    context = {'form': form}
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            word_to_anagram = form.cleaned_data.get('anagrams_letters').strip().lower()
            
            word_list = None

            # going through scrabble dictionary to use this as the basis for finding anagrams
            with open("ospd.txt", "r") as file:
                word_list = file.readlines()
            
            t = My_Trie()

            processed_words = [word.strip() for word in word_list if len(word.strip()) >= SCRABBLE_START and len(word.strip()) <= len(word_to_anagram)]

            for word in processed_words:
                t.insert(word)
                    
            
            # finding what amounts to the powerset of the word's chars to
            # find out whether each combination of words counts as an actual
            # word in the OSPD
            word_to_anagram_permutations= []
            for i in range(SCRABBLE_START, len(word_to_anagram) + 1, 1):
                for perm in it.permutations(word_to_anagram.strip().lower(), i):
                    word_to_anagram_permutations.append("".join(perm))
            
            word_to_anagram_combinations = []

            for word in word_to_anagram_permutations:
                for i in range(SCRABBLE_START, len(word_to_anagram) + 1, 1):
                    word_to_anagram_combinations += list(it.combinations(word, i))
            
            word_to_anagram_strings = []

            for word in word_to_anagram_combinations:
                word_to_anagram_strings.append("".join(word))

            # eliminating duplicates
            word_to_anagram_strings = list(set(word_to_anagram_strings))
            
            anagrams = []

            # checking to see if all anagrams combos are a valid word in the OSPD,
            # and therefore if it is a valid anagram
            for word in word_to_anagram_strings:
                if t.is_word(word):
                    anagrams.append(word)

            anagrams.sort(reverse=True, key=len)

            context['anagrams_results'] = anagrams
            context['anagrams_letters'] = word_to_anagram
            context['anagrams_no_solutions'] = 'There are no words with the requested letters.\n'

        else:
            form = AnagramsForm(request.POST or None)

    return render(request, 'anagrams.html', context)

def boggle(request):
    form = BoggleForm(request.POST or None)
    context = {'form': form}
    if request.method == 'POST':
        if form.is_valid():
            form.save()

            # initializes boggle board with user input
            boggle_board = np.chararray((4, 4))

            boggle_board[0,0] = form.cleaned_data.get('boggle_11').lower()
            boggle_board[0,1] = form.cleaned_data.get('boggle_12').lower()
            boggle_board[0,2] = form.cleaned_data.get('boggle_13').lower()
            boggle_board[0,3] = form.cleaned_data.get('boggle_14').lower()

            boggle_board[1,0] = form.cleaned_data.get('boggle_21').lower()
            boggle_board[1,1] = form.cleaned_data.get('boggle_22').lower()
            boggle_board[1,2] = form.cleaned_data.get('boggle_23').lower()
            boggle_board[1,3] = form.cleaned_data.get('boggle_24').lower()

            boggle_board[2,0] = form.cleaned_data.get('boggle_31').lower()
            boggle_board[2,1] = form.cleaned_data.get('boggle_32').lower()
            boggle_board[2,2] = form.cleaned_data.get('boggle_33').lower()
            boggle_board[2,3] = form.cleaned_data.get('boggle_34').lower()

            boggle_board[3,0] = form.cleaned_data.get('boggle_41').lower()
            boggle_board[3,1] = form.cleaned_data.get('boggle_42').lower()
            boggle_board[3,2] = form.cleaned_data.get('boggle_43').lower()
            boggle_board[3,3] = form.cleaned_data.get('boggle_44').lower()

            #print(boggle_board)
            my_trie = create_trie()
            words = solver(boggle_board, my_trie)
            context['boggle_solution'] = words
            context['num_words'] = len(words)
            context['boggle_no_solutions'] = 'There are no words with the requested letters.\n'
            
            boggle_list = [
                form.cleaned_data.get('boggle_11').lower(),
                form.cleaned_data.get('boggle_12').lower(),
                form.cleaned_data.get('boggle_13').lower(),
                form.cleaned_data.get('boggle_14').lower(),

                form.cleaned_data.get('boggle_21').lower(),
                form.cleaned_data.get('boggle_22').lower(),
                form.cleaned_data.get('boggle_23').lower(),
                form.cleaned_data.get('boggle_24').lower(),

                form.cleaned_data.get('boggle_31').lower(),
                form.cleaned_data.get('boggle_32').lower(),
                form.cleaned_data.get('boggle_33').lower(),
                form.cleaned_data.get('boggle_34').lower(),

                form.cleaned_data.get('boggle_41').lower(),
                form.cleaned_data.get('boggle_42').lower(),
                form.cleaned_data.get('boggle_43').lower(),
                form.cleaned_data.get('boggle_44').lower(),
            ]

            context['boggle_input'] = boggle_list

        else:
            form = BoggleForm(request.POST or None)
    return render(request, 'boggle.html', context)

def wordscape(request):
    form = WordscapeForm(request.POST or None)
    context = {'form': form}
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            wordscape_chars = form.cleaned_data.get('wordscape_letters').strip().lower()
            length_check = False
            word_size = form.cleaned_data.get('wordscape_length')
            if word_size != None:
                length_check = True

            # oxford will have the entire applicable dictionary of related words within it
            oxford = My_Trie()

            # t will be the Trie to which we add words which are anagrams
            t = My_Trie()

            # word_search_space will be all applicable words of a certain size 
            word_search_space = []

            with open("ospd.txt", "r") as file:
                word_list = file.readlines()

            for word in word_list:
                word = word.strip()

                # only allowing words that are longer than 2 chars and shorter than
                # the word we're trying to anagram
                if (length_check and len(word) == word_size) or not length_check:
                    if len(word) >= SCRABBLE_START:
                        word_search_space.append(word)
                        oxford.insert(word)
                        
            find_anagram_words(oxford, t, sorted(wordscape_chars), "")

            wordscapes_solutions = dict.fromkeys([num for num in range(SCRABBLE_START, len(wordscape_chars) + 1, 1)])

            for key in wordscapes_solutions.keys():
                wordscapes_solutions[key] = []

            for word in word_search_space:
                if t.is_word(word):
                    if (length_check and len(word) == word_size) or not length_check:
                        wordscapes_solutions[len(word)].append(word)

            wordscapes_list = []
            context_list = []

            if word_size == None:
                # for i in range(SCRABBLE_START, len(wordscape_chars) + 1, 1):
                #     length_list = wordscapes_solutions.get(i)
                #     for j in length_list:
                #         context_list.append(j)
                # context["wordscape_results"] = context_list
                context['wordscape_results'] = wordscapes_solutions
            else:
                context['wordscape_results_len'] = wordscapes_solutions[word_size]
            
            context['wordscape_letters'] = wordscape_chars
            context['wordscape_no_solutions'] = 'There are no words with the requested letters.\n'
    
    return render(request, 'wordscape.html', context)

def general(request):
    context = {}
    return render(request, 'general.html', context)


# HELPER METHODS
def find_anagram_words(oxford, t, word_to_anagram, text):
    for i in range(0, len(word_to_anagram), 1):
        text1 = text + word_to_anagram[i]
        if oxford.is_prefix(text1) and not t.is_prefix(text1):
            if oxford.is_word(text1):
                t.insert(text1)
            text2 = word_to_anagram[0:i] + word_to_anagram[i + 1:]
            find_anagram_words(oxford, t, text2, text1)

def wordle_char_locations(char_locations, form, loc):
    if (form.cleaned_data.get(loc) != None):
        char_locations.append(form.cleaned_data.get(loc).strip().lower())
    else:
        char_locations.append('_')

def find_boggle_score(solved_word):
    if len(solved_word) < 3:
        return 0
    elif len(solved_word) < 5:
        return 1
    elif len(solved_word) < 6:
        return 2
    elif len(solved_word) < 7:
        return 3
    elif len(solved_word) < 8:
        return 4
    else:
        return 11

def solverRecursive(board, visited, dictionary, x, y, my_string, boggle_solution, path_list):
    # mark visited, append current square number to list
    visited[x][y] = True
    cur_square = 4 * x + y + 1
    path_list.append(cur_square)
    # update string with letter on board
    tempstr = board[x][y].decode("utf-8")
    my_string += tempstr
    #  print if word
    if dictionary.is_word(my_string):
        path_list_copy = path_list.copy()
        boggle_solution.update({my_string: path_list_copy})

    # traverse adjacent cells to current cell
    # move index to row above i
    if dictionary.is_prefix(my_string):
        rowIndex = x - 1
        while rowIndex <= x + 1 and rowIndex < BOGGLE_SIDE_LEN:
            colIndex = y - 1
            while colIndex <= y + 1 and colIndex < BOGGLE_SIDE_LEN:
                if rowIndex >= 0 and colIndex >= 0 and not visited[rowIndex][colIndex]:
                    solverRecursive(board, visited, dictionary, rowIndex, colIndex, my_string, boggle_solution, path_list)
                colIndex += 1
            rowIndex += 1

    
    path_list.remove(cur_square)
    my_string = "" + my_string[-1]
    visited[x][y] = False

def solver(board, dictionary):
    # creates array of visited cells initialized to false
    visited = np.full((4, 4), False)
    boggle_solution = {}
    #   print(visited)

    temp_string = ""
    path_list = []

    # nested for loop traversing through all letters on boggle board
    for a in range(BOGGLE_SIDE_LEN):
        for b in range(BOGGLE_SIDE_LEN):
            solverRecursive(board, visited, dictionary, a, b, temp_string, boggle_solution, path_list)
            visited[:] = False
    return boggle_solution

def create_trie():
    # creates list where each word in dictionary is an item in the list
    with open("boggle_dict.txt", "r") as file:
        word_list = file.readlines()

    # initializes Trie
    oxford = My_Trie()

    # removes all leading and trailing whitespace for each word in list
    for new_word in word_list:
        new_word = new_word.strip()
        new_word = new_word.lower()
        # only allowing words that are longer than 2 chars and shorter than
        # the max length of a Boggle word (16 chars)
        if BOGGLE_WORD_MAX >= len(new_word) > BOGGLE_WORD_MIN:
            # inserts words into Trie form word_list
            oxford.insert(new_word)
    return oxford

def scrabble_processing(word_dict, processed_list, chars_on_board, user_chars):

    for word in processed_list:
        user_chars_copy = user_chars.copy()
        chars_on_board_copy = chars_on_board.copy()

        used_chars = []

        for char in word:
            if char in user_chars_copy:
                user_chars_copy.remove(char)
                used_chars.append(char)
        
        # checking to see if every letter of the word except for one on the board
        # comes from the user's current hand

        if len(used_chars) == (len(word) - 1):
            for char in word:

                # checking for final character that we need to complete the word
                # here it's assumed that the character should be on the board and
                # isn't in used_chars
                if char in chars_on_board_copy and char not in used_chars:
                    chars_on_board_copy.remove(char)
                    used_chars.append(char)

        # accounting for case where all the letters are in the hand to make a word
        # just in case there is a letter on the board that matches what was in your hand
        elif len(used_chars) == len(word):
            for char in used_chars:
                if char in chars_on_board_copy:
                    # calculating the scrabble word score - this is self-explanatory, method's further below
                    score = find_scrabble_base_word_score(word)

                    # if there are no words for a particular score, initialize this key-value pair so we
                    # can add words of a certain score later.
                    if score not in word_dict.keys():
                        word_dict[score] = []
                                
                    # adding a word to the list which makes up the value to the key of a specific score
                    word_dict[score].append(word)
                    break
            continue
        else:
            continue

        
        if sorted(word) == sorted("".join(used_chars)):

            # calculating the scrabble word score - this is self-explanatory, method's further below
            score = find_scrabble_base_word_score(word)

            # if there are no words for a particular score, initialize this key-value pair so we
            # can add words of a certain score later.
            if score not in word_dict.keys():
                word_dict[score] = []
                        
            # adding a word to the list which makes up the value to the key of a specific score
            word_dict[score].append(word)

def find_scrabble_base_word_score(word):
    score = 0
    for char in word:
        score += SCRABBLE_LETTER_SCORES[char]
    return score