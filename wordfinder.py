from math import ceil
from trie_test import My_Trie
from timeit import repeat
import numpy as np
import itertools as it

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

def scrabble_main():
    user_chars = input("Enter your characters: ")
    chars_on_board = input("Enter open characters on board you think have potential: ")
    with open("ospd.txt", "r") as file:
        word_list = file.readlines()

    processed_list = [word.strip() for word in word_list if (len(word.strip()) >= SCRABBLE_START and len(word.strip()) <= SCRABBLE_END)]

    user_chars = "".join(set(user_chars.strip()))
    chars_on_board = "".join(set(chars_on_board.strip()))

    word_dict = {}

    print("\n\nFinding your words...\n")
    scrabble_processing_updated(word_dict, processed_list, chars_on_board, user_chars)

    keys_list = [key for key in word_dict.keys()]
    keys_list.sort(reverse=True)

    print("Printing your words...")
    for key in keys_list:
        print(f'Scrabble solutions of score {key}:\n')
        print(*word_dict[key], sep=', ')
        print('\n')

        
def scrabble_processing_updated(word_dict, processed_list, chars_on_board, user_chars):

    # it appears that this solution works so I'm leaving comments to endeavor to explain how
    # it actually finds scrabble words; this is an arbitrary cutoff 

    # removing duplicated characters

    char_counter = 0
    repeat_letters = 0

    # removing duplicated characters
    char_set = "".join(set(user_chars))
    char_counter = 0
    repeat_letters = 0

    for word in processed_list:
        
        # this is an arbitray cutoff for the number of characters a word must have from both
        # the characters the user has in their hand and the characters on the board that the user
        # wants to find a word to make. I set it at around 2/3 of the characters matching
        # which I think is fair enough. I account for repeats later.
        char_bound = ceil(2*len(word)/3)
        
        # python idiom to remove repeating characters from a word
        word_with_no_repeats = "".join(set(word))

        # here I calculate the number of repeating characters, basically just adding up the occurrences
        # of a character for each character in the word. I calculate the count for each word and fine
        # the repeat_letters of that word by taking the number of occurrences, I just increment repeat_letters
        # by one.
        for char in word_with_no_repeats:
            if word.count(char) > 1:
                repeat_letters += 1


        for i in range(0, len(word), 1):

                # if a character is found in the word that is in the combined set of characters
                # on the board that the user thinks is high potential or in the set of characters
                # in the user's hand, increment char_counter
            if char_set.find(word[i]) > -1:
                char_counter += 1
            
            if char_counter >= char_bound + repeat_letters and char_counter <= len(word):
                
                for char in word:
                    if ((chars_on_board.find(char) > -1 and word.count(char) > 1)
                        or (chars_on_board.find(char) > -1 and user_chars.find(char) == -1)):

                        # calculating the scrabble word score - this is self-explanatory, method's further below
                        score = find_scrabble_base_word_score(word)

                        # if there are no words for a particular score, initialize this key-value pair so we
                        # can add words of a certain score later.
                        if score not in word_dict.keys():
                            word_dict[score] = []
                        
                        # adding a word to the list which makes up the value to the key of a specific score
                        word_dict[score].append(word)

                        # resetting the counting variables for the next word and breaking from the loop 
                        # of analyzing each character when we have seen enough
                        char_counter = 0
                        repeat_letters = 0
                        break
        
        # resetting the counting variables for the next word just in case a word doesn't fit
        # with the letters the user has on the board / in their hand
        char_counter = 0
        repeat_letters = 0




def find_scrabble_base_word_score(word):
    score = 0
    for char in word:
        score += SCRABBLE_LETTER_SCORES[char]
    return score

def wordle():

    char_locations = []
    char_list = ['a', 'b', 'c', 'd', 'e', 'f']
    while(len(char_locations) != 5):
        char_locations = input("Enter locations of letters with unknown letters as underscores: ")

    num_known_characters = 0
    for i in range(0, WORDLE_LEN, 1):
                if char_locations[i] != "_":
                    num_known_characters = num_known_characters + 1

    while(len(char_list) + num_known_characters > WORDLE_LEN):
        char_list = input("Enter characters: ")
    
    check_for_invalid_letters = ""
    invalid_chars = ""
    
    # optional prompting to allow for users to enter letters that they know are invalid
    input_valid_for_invalid_letters = False
    check_for_invalid_letters = input("Do you want to enter characters that you know are invalid? (y/n) ").strip().lower()
    while not input_valid_for_invalid_letters:
        if check_for_invalid_letters == "n" or check_for_invalid_letters == "no":
            input_valid_for_invalid_letters = True
            break
        elif check_for_invalid_letters == "y" or check_for_invalid_letters == "yes":
            input_valid_for_invalid_letters = True

            # using set feature to eliminate letters that were entered multiple times and reduce them to one letter
            invalid_chars = list(set(input("Enter characters that you know are invalid: ").strip().lower()))
        else:
            check_for_invalid_letters = input("Invalid input - Do you want to enter characters that you know are invalid? (y/n) ").strip().lower()
    
    print(invalid_chars)
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
        print('Potential Wordle words with requested letters:')
        print(*filtered_wordle_solutions, sep=", ")
        print()  
    elif not invalid_chars and wordle_solutions:
        print('Potential Wordle words with requested letters:')
        print(*wordle_solutions, sep=", ")
        print()
    else:
        print('There are no words with the requested letters.\n')


def anagrams():

    # taking input from user for word with which to find anagrams
    word_to_anagram = input("Enter your word for which to find anagrams: ")
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

    print(word_to_anagram_permutations)
    
    word_to_anagram_combinations = []

    for word in word_to_anagram_permutations:
        for i in range(SCRABBLE_START, len(word_to_anagram) + 1, 1):
            word_to_anagram_combinations += list(it.combinations(word, i))
    
    word_to_anagram_strings = []

    for word in word_to_anagram_combinations:
        word_to_anagram_strings.append("".join(word))

    # eliminating duplicates
    word_to_anagram_strings = list(set(word_to_anagram_strings))
    
    print(word_to_anagram_strings)
    anagrams = []

    # checking to see if all anagrams combos are a valid word in the OSPD,
    # and therefore if it is a valid anagram
    for word in word_to_anagram_strings:
        if t.is_word(word):
            anagrams.append(word)

    anagrams.sort(reverse=True, key=len)

    print(f"Here are your anagrams for {word_to_anagram}\n{anagrams}")


# here's another implementation of anagrams with a Trie data structure 
# just to check which implementation is faster
def anagrams_trie():

    # taking input from user for word with which to find anagrams
    word_to_anagram = input("Enter your word for which to find anagrams: ")
    word_list = None

    # oxford will have the entire applicable dictionary of related words within it
    oxford = My_Trie()

    # t will be the Trie to which we add words which are anagrams
    t = My_Trie()

    word_dict = dict.fromkeys([num for num in range(SCRABBLE_START, len(word_to_anagram) + 1, 1)])
    anagrams_solutions = dict.fromkeys([num for num in range(SCRABBLE_START, len(word_to_anagram) + 1, 1)])
    for key in word_dict.keys():
        word_dict[key] = []
        anagrams_solutions[key] = []

    print("Processing dictionary...\n\n")
    # going through scrabble dictionary to use this as the basis for finding anagrams
    with open("ospd.txt", "r") as file:
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
        if len(word) <= len(word_to_anagram) and len(word) >= SCRABBLE_START:
            word_dict[len(word)].append(word)
            oxford.insert(word)
    
    print("\n\nFinding your words...\n\n")
    # helper function allowing us to find permutations;
    # python is all pass-by-reference so this works fine
    find_anagram_words(oxford, t, sorted(word_to_anagram), "")

    for key in word_dict.keys():
        for word in word_dict[key]:
            if t.is_word(word):
                anagrams_solutions[len(word)].append(word)

    for i in range(SCRABBLE_START, len(word_to_anagram) + 1, 1):
        if anagrams_solutions[i]:
            print(f'\nPotential anagrams of {word_to_anagram} with {i} characters:')
            print(*anagrams_solutions[i], sep=', ')
            print()
        else:
            print(f'\nThere are no anagrams of {word_to_anagram} with {i} characters')


def find_anagram_words(oxford, t, word_to_anagram, text):

    for i in range(0, len(word_to_anagram), 1):
        text1 = text + word_to_anagram[i]
        if oxford.is_prefix(text1) and not t.is_prefix(text1):
            if oxford.is_word(text1):
                t.insert(text1)
            text2 = word_to_anagram[0:i] + word_to_anagram[i + 1:]
            find_anagram_words(oxford, t, text2, text1)

# this game is like anagrams but sets a parameter and allows you
# to find all the anagrams of a certain length
def wordscapes():
    wordscape_chars = input("Enter your wordscape characters: ").strip().lower()

    length_check = False

    while True:
        try:
            user_input = input("Do you want words of only a specific length? (Enter y/n): ")
            u = user_input.strip().lower()
            if u == "y" or u == "yes":
                length_check = True
                break
            elif u == "n" or u == "no":
                break
            else:
                print("Incorrect input - please enter y/n\n")
        except ValueError:
            print("Incorrect input - please enter y/n\n")

    if length_check:
        word_size = int(input("What size word are you looking for? Enter a number: ").strip())

    # oxford will have the entire applicable dictionary of related words within it
    oxford = My_Trie()

    # t will be the Trie to which we add words which are anagrams
    t = My_Trie()

    # word_search_space will be all applicable words of a certain size 
    word_search_space = []

    with open("words.txt", "r") as file:
        word_list = file.readlines()

    print("\n\nProcessing dictionary...\n")
    for word in word_list:
        word = word.strip()

        # only allowing words that are longer than 2 chars and shorter than
        # the word we're trying to anagram
        if (length_check and len(word) == word_size) or not length_check:
            if len(word) >= SCRABBLE_START:
                word_search_space.append(word)
                oxford.insert(word)
                
    print("\n\nFinding your words...\n")
    find_anagram_words(oxford, t, sorted(wordscape_chars), "")

    wordscapes_solutions = dict.fromkeys([num for num in range(SCRABBLE_START, len(wordscape_chars) + 1, 1)])

    for key in wordscapes_solutions.keys():
        wordscapes_solutions[key] = []

    for word in word_search_space:
        if t.is_word(word):
            if (length_check and len(word) == word_size) or not length_check:
                wordscapes_solutions[len(word)].append(word)

    for i in range(SCRABBLE_START, len(wordscape_chars) + 1, 1):
        if wordscapes_solutions[i]:
            print(f'Potential wordscape words of {i} characters with your letters:')
            print(*wordscapes_solutions[i], sep=', ')
            print()
        else:
            print(f'There are no words with {i} characters and the requested letters\n')


def create_trie():
    # creates list where each word in dictionary is an item in the list
    with open("words.txt", "r") as file:
        word_list = file.readlines()

    # initializes Trie
    oxford = My_Trie()

    # removes all leading and trailing whitespace for each word in list
    for new_word in word_list:
        new_word = new_word.strip()
        # only allowing words that are longer than 2 chars and shorter than
        # the max length of a Boggle word (16 chars)
        if BOGGLE_WORD_MAX >= len(new_word) > BOGGLE_WORD_MIN:
            # inserts words into Trie form word_list
            oxford.insert(new_word)
    return oxford

    # for word in boggle_list:
    #  print(f"{word} --> score: {find_boggle_score(word)}")


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


def solverRecursive(board, visited, dictionary, x, y, my_string):
    # mark visited
    visited[x][y] = True
    # update string with letter on board
    tempstr = board[x][y].decode("utf-8")
    my_string += tempstr
    #  print if word
    if dictionary.is_word(my_string):
        print(my_string)

    # traverse adjacent cells to current cell
    # move index to row above i
    if dictionary.is_prefix(my_string):
        rowIndex = x - 1
        while rowIndex <= x + 1 and rowIndex < BOGGLE_SIDE_LEN:
            colIndex = y - 1
            while colIndex <= y + 1 and colIndex < BOGGLE_SIDE_LEN:
                if rowIndex >= 0 and colIndex >= 0 and not visited[rowIndex][colIndex]:
                    solverRecursive(board, visited, dictionary, rowIndex, colIndex, my_string)
                colIndex += 1
            rowIndex += 1

    my_string = "" + my_string[-1]
    visited[x][y] = False


def solver(board, dictionary):
    # creates array of visited cells initialized to false
    visited = np.full((4, 4), False)
    #   print(visited)

    temp_string = ""

    # nested for loop traversing through all letters on boggle board
    for a in range(BOGGLE_SIDE_LEN):
        for b in range(BOGGLE_SIDE_LEN):
            solverRecursive(board, visited, dictionary, a, b, temp_string)
            visited[:] = False

def boggle_start():
    # initializes boggle board with user input
    boggle_board = np.chararray((4, 4))

    for i in range(0, BOGGLE_SIDE_LEN, 1):
        for j in range(0, BOGGLE_SIDE_LEN, 1):
            boggle_board[i][j] = input("Enter letter: ")

    print(boggle_board)
    my_trie = create_trie()
    solver(boggle_board, my_trie)




# def boggle_and_wordhunt():
#     boggle_board = []
#     for i in range(0, BOGGLE_SIDE_LEN, 1):
#         end_term = "st" if i == 0 else ("nd" if (i == 1) else ("rd" if (i == 2) else "th"))
#         boggle_board.append(input(f"Enter your {i + 1}{end_term} row: ").strip().lower().split())
#
#     word_list = []
#
#     with open("words.txt", "r") as file:
#         word_list = file.readlines()
#
#     word_dict = dict.fromkeys([num for num in range(SCRABBLE_START, BOGGLE_WORD_MAX + 1, 1)])
#     oxford = My_Trie()
#
#     for word in word_list:
#         word = word.strip()
#
#         # only allowing words that are longer than 2 chars and shorter than
#         # the max length of a Boggle word (16 chars)
#         if len(word) <= BOGGLE_WORD_MAX and len(word) > SCRABBLE_START:
#             word_dict[len(word)].append(word)
#             oxford.insert(word)
#
#     boggle_list = []
#
#     for word in boggle_list.sort(key=len):
#         print(f"{word}")

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
    scrabble_main()