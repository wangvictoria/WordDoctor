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
PATH = "/Users/shaneausmus/Desktop/Vandy Course Materials/Spring 2022/CS 4279/WordDoctor"
SCRABBLE_LETTER_SCORES = {"A": 1, "E": 1, "I": 1, "O": 1, "U": 1, "L": 1, "N": 1,
                        "S": 1, "T": 1, "R": 1, "D": 2, "G": 2, "B": 3, "C": 3,
                        "M": 3, "P": 3, "F": 4, "H": 4, "V": 4, "W": 4, "Y": 4,
                        "K": 5, "J": 8, "X": 8, "Q": 10, "Z": 10} 

# Thinking about trying to time how long finding characters in all the words would take in
# Python with multi-threading and with the standard approach I outline below using one of
# the timer modules; check out this article https://realpython.com/python-timer/


# Need solution for following games:
# Scrabble --> approaching completion
# Wordle --> DONE
# Anagrams --> DONE
# Boggle / WordHunt
# WordBrain (superset of Boggle functionality)
# Wordscape --> DONE

def main_scrabble():
    user_chars = input("Enter your characters: ")
    chars_on_board = input("Enter open characters on board you think have potential: ")
    with open(f"{PATH}/ospd.txt", "r") as file:
        
        mp.set_start_method('spawn')
        manager = mp.Manager()

        word_list = file.readlines()
        substr = "".join(user_chars)

        chars_on_board_set = "".join(set(chars_on_board))

        word_dict_sequential = manager.dict()
        for i in range(SCRABBLE_START, SCRABBLE_END + 1, 1):
            word_dict_sequential[i] = np.array([])

        word_dict_out_of_order = manager.dict()
        for i in range(SCRABBLE_START, SCRABBLE_END + 1, 1):
            word_dict_out_of_order[i] = np.array([])

        t1 = mp.Process(target=scrabble_sequential, args=(word_dict_sequential,
                                                                            chars_on_board_set,
                                                                            substr,
                                                                            word_list))
        t2 = mp.Process(target=scrabble_out_of_order, args=(word_dict_out_of_order,
                                                                                chars_on_board_set,
                                                                                substr,
                                                                                word_list))
        
        t1.start()
        t2.start()

        t1.join()
        t2.join()

        print(word_dict_sequential)
        print(word_dict_out_of_order)

        print("\n\nFinding your words...\n")
        for i in range(SCRABBLE_START, SCRABBLE_END + 1, 1):
            if word_dict_sequential[i]:
                print(f'Words of size {i} with your letters (sequentially):')
                print(*word_dict_sequential[i], sep='\n')
                print()
            else:
                print(f'There are no words of size {i} with the requested letters sequentially.\n')

            if word_dict_out_of_order[i]:
                print(f'Potential words with requested letters (out-of-order):')
                print(*word_dict_out_of_order, sep='\n')
                print()
            else:
                print(f'There are no words of size {i} with the requested letters out of order.\n')
                

# def scrabble_sequential(word_dict_sequential, chars_on_board_set, substr, word_list): 

#     for word in word_list:
#         word = word.strip()
#         if substr in word:
#             a = word_dict_sequential[len(word)]
#             a = np.append(a, word)
#             word_dict_sequential[len(word)] = a


#     # sequential word processing
#     for key in word_dict_sequential.keys():
#         for word in word_dict_sequential[key]:
#             for i in range(0, len(chars_on_board_set), 1):
#                 if chars_on_board_set[i] in word:
#                     break
#                 if i == len(chars_on_board_set) - 1:
#                     a = word_dict_sequential[len(word)]
#                     for i in range(0, len(a, 1)):
#                         if a[i] == word:
#                             a = np.delete(a, i)
#                             break
#                     word_dict_sequential[len(word)] = a
#     print (word_dict_sequential)


def scrabble_out_of_order(word_dict_out_of_order, chars_on_board_set, substr, word_list):

    for word in word_list:
        word = word.strip()
        for i in range(0, len(substr), 1):
            if substr[i] not in word:
                break
            if i == len(substr) - 1:
                a = word_dict_out_of_order[len(word)]
                a = np.append(a, word)
                word_dict_out_of_order[len(word)] = a
                
    # out_of_order word processing
    for key in word_dict_out_of_order.keys():
        for word in word_dict_out_of_order[key]:
            for i in range(0, len(chars_on_board_set), 1):
                if chars_on_board_set[i] in word:
                    break
                if i == len(chars_on_board_set) - 1:
                    a = word_dict_out_of_order[len(word)]
                    for i in range(0, len(a, 1)):
                        if a[i] == word:
                            a = np.delete(a, i)
                            break
                    word_dict_out_of_order[len(word)] = a

    print (word_dict_out_of_order)


def wordle():
    while True:
            try:
                char_list = input("Enter characters: ")
                if len(char_list) > WORDLE_LEN or len(char_list) <= 0:
                    print("Wordle words must be less than or equal to 5 characters; try again!")
                else:
                    break
            except ValueError:
                print("This input does not meet the required 1 to 5 characters for a Wordle word")


    with open(f"{PATH}/wordle.txt", "r") as file:
        word_list = file.readlines()
        substr = "".join(char_list)

        words_with_in_order_chars = []
        words_with_out_of_order_chars = []

        # performing search for sequences of letters in order
        for word in word_list:
            word = word.strip()
            if substr in word:
                words_with_in_order_chars.append(word)
            for i in range(0, len(char_list), 1):
                if char_list[i] not in word:
                    break
                if i == len(char_list) - 1:
                    words_with_out_of_order_chars.append(word)
                
        if words_with_in_order_chars:
            print(f'Potential Wordle words with requested letters (sequentially):')
            print(*words_with_in_order_chars, sep='\n')
            print()
        if words_with_out_of_order_chars:
            print(f'Potential Wordle words with requested letters (out-of-order):')
            print(*words_with_out_of_order_chars, sep='\n')
            print()
            
        if not words_with_in_order_chars and not words_with_out_of_order_chars:
            print(f'There are no words with the requested letter sequence.\n')


def anagrams():

    # taking input from user for word with which to find anagrams
    word_to_anagram = input("Enter your word for which to find anagrams: ")
    word_list = None

    # going through scrabble dictionary to use this as the basis for finding anagrams
    with open(f"{PATH}/ospd.txt", "r") as file:
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

    print(f"Here are your anagrams for {word_to_anagram}\n{anagrams}")


# here's another implementation of anagrams with a Trie data structure 
# just to check which implementation is faster
def anagrams_trie():

    # taking input from user for word with which to find anagrams
    word_to_anagram = input("Enter your word for which to find anagrams: ")
    word_list = None

    # oxford will have the entire applicable dictionary of related words within it
    oxford = Trie()

    # t will be the Trie to which we add words which are anagrams
    t = Trie()

    word_dict = dict.fromkeys([num for num in range(SCRABBLE_START + 1, len(word_to_anagram) + 1, 1)])

    for key in word_dict.keys():
        word_dict[key] = []

    # going through scrabble dictionary to use this as the basis for finding anagrams
    with open(f"{PATH}/words.txt", "r") as file:
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

    print(f"Here are your anagrams for {word_to_anagram}\n{anagrams}")

def find_anagram_words(oxford, t, word_to_anagram, text):

    for i in range(0, len(word_to_anagram), 1):
        text1 = text + word_to_anagram[i]
        if oxford.contains(text1) and not t.contains(text1):
            t.add(text1)
            text2 = word_to_anagram[0:i] + word_to_anagram[i + 1:]
            find_anagram_words(oxford, t, text2, text1)

# this game is like anagrams but sets a parameter and allows you
# to find all the anagrams of a certain length
def wordscape():
    wordscape_chars = input("Enter your wordscape characters: ").strip().lower()
    word_size = int(input("What size word are you looking for? Enter a number: ").strip())

    # oxford will have the entire applicable dictionary of related words within it
    oxford = Trie()

    # t will be the Trie to which we add words which are anagrams
    t = Trie()

    # word_search_space will be all applicable words of a certain size 
    word_search_space = []

    with open(f"{PATH}/words.txt", "r") as file:
        word_list = file.readlines()

    for word in word_list:
        word = word.strip()

        # only allowing words that are longer than 2 chars and shorter than
        # the word we're trying to anagram
        if len(word) == word_size:
            word_search_space.append(word)
            oxford.add(word)
    
    find_anagram_words(oxford, t, sorted(wordscape_chars), "")

    wordscapes_solutions = []

    for word in word_search_space:
        if t.contains(word):
            wordscapes_solutions.append(word)

    print(f"Here are your anagrams for {wordscape_chars}\n{wordscapes_solutions}")

def boggle_and_wordhunt():
    boggle_board = []
    for i in range(0, BOGGLE_SIDE_LEN, 1):
        end_term = "st" if i == 0 else ("nd" if (i == 1) else ("rd" if (i == 2) else "th"))
        boggle_board.append(input(f"Enter your {i + 1}{end_term} row: ").strip().lower().split())

    word_list = []

    with open(f"{PATH}/words.txt", "r") as file:
        word_list = file.readlines()

    word_dict = dict.fromkeys([num for num in range(SCRABBLE_START + 1, BOGGLE_WORD_MAX + 1, 1)])
    oxford = Trie()

    for word in word_list:
        word = word.strip()

        # only allowing words that are longer than 2 chars and shorter than
        # the max length of a Boggle word (16 chars)
        if len(word) <= BOGGLE_WORD_MAX and len(word) > SCRABBLE_START:
            word_dict[len(word)].append(word)
            oxford.add(word)

    boggle_list = []

    for word in boggle_list.sort(key=len):
        print(f"{word}")

# def find_boggle_score(word):
#     if len(word) < 3:
#         return 0
#     elif len(word) < 5:
#         return 1
#     elif len(word) < 6:
#         return 2
#     elif len(word) < 7:
#         return 3
#     elif len(word) < 8:
#         return 4
#     else:
#         return 11

if __name__ == "__main__":
    anagrams_trie()