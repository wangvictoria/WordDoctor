from gettext import npgettext
import multiprocessing as mp
from multiprocessing.dummy import Process, Manager
from python_datastructures import Trie
import numpy as np
import itertools as it

SCRABBLE_START = 2
SCRABBLE_END = 15
WORDLE_LEN = 5
ALPHABET_START = 1
ALPHABET_END = 26
PATH = "/Users/shaneausmus/Desktop/Vandy Course Materials/Spring 2022/CS 4279"

# Thinking about trying to time how long finding characters in all the words would take in
# Python with multi-threading and with the standard approach I outline below using one of
# the timer modules; check out this article https://realpython.com/python-timer/


# Need solution for following games:
# Scrabble --> approaching completion
# Wordle --> DONE
# Anagrams --> DONE
# Boggle / WordHunt
# Wordscape

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
        # t2 = mp.Process(target=scrabble_out_of_order, args=(word_dict_out_of_order,
        #                                                                        chars_on_board_set,
        #                                                                        substr,
        #                                                                        word_list))
        
        t1.start()
        #t2.start()

        t1.join()
        #t2.join()

        print(word_dict_sequential)
       # print(word_dict_out_of_order)

        print("\n\nFinding your words...\n")
        for i in range(SCRABBLE_START, SCRABBLE_END + 1, 1):
            if word_dict_sequential[i]:
                print(f'Words of size {i} with your letters (sequentially):')
                print(*word_dict_sequential[i], sep='\n')
                print()
            else:
                print(f'There are no words of size {i} with the requested letters sequentially.\n')

            # if word_dict_out_of_order[i]:
            #     print(f'Potential words with requested letters (out-of-order):')
            #     print(*word_dict_out_of_order, sep='\n')
            #     print()
            # else:
            #     print(f'There are no words of size {i} with the requested letters out of order.\n')
                

def scrabble_sequential(word_dict_sequential, chars_on_board_set, substr, word_list): 

    for word in word_list:
        word = word.strip()
        if substr in word:
            a = word_dict_sequential[len(word)]
            a = np.append(a, word)
            word_dict_sequential[len(word)] = a


    # sequential word processing
    for key in word_dict_sequential.keys():
        for word in word_dict_sequential[key]:
            for i in range(0, len(chars_on_board_set), 1):
                if chars_on_board_set[i] in word:
                    break
                if i == len(chars_on_board_set) - 1:
                    a = word_dict_sequential[len(word)]
                    for i in range(0, len(a, 1)):
                        if a[i] == word:
                            a = np.delete(a, i)
                            break
                    word_dict_sequential[len(word)] = a
    print (word_dict_sequential)


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

        words_with_in_order_chars = np.array([])
        words_with_out_of_order_chars = np.array([])

        # performing search for sequences of letters in order
        for word in word_list:
            word = word.strip()
            if substr in word:
                a = np.append(words_with_in_order_chars, word)
                words_with_in_order_chars = a
            for i in range(0, len(char_list), 1):
                if char_list[i] not in word:
                    break
                if i == len(char_list) - 1:
                    a = np.append(words_with_out_of_order_chars, word)
                    words_with_out_of_order_chars = a
                
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

    # using python_datastructures package for this implementation 
    t = Trie()
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
            t.add(word)
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

    print(word_to_anagram_permutations_strings)
    
    anagrams = []

    # checking to see if all anagrams combos are a valid word in the OSPD,
    # and therefore if it is a valid anagram
    for word in word_to_anagram_permutations_strings:
        if word in word_dict[len(word)]:
            anagrams.append(word)

    print(f"Here are your anagrams for {word_to_anagram}\n{anagrams}")



if __name__ == "__main__":
    anagrams()