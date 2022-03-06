class Node:
    __slots__ = ('char', 'children', 'word')

    def __init__(self, char):
        self.char = char
        self.children = {}
        self.word = False
    
    
    def is_word(self, word):
        if (len(word) == 1):
            if word in self.children:
                return self.children[word].word
            else:
                return False
        else:
            if word[0] in self.children:
                return self.children[word[0]].is_word(word[1:])
            else:
                return False

    def is_prefix(self, word):
        if (len(word) == 1):
            if word in self.children:
                # Commented line is for if we don't want to include a word as its own prefix
                # return bool(self.children[word].children)
                return True
            else:
                return False
        else:
            if word[0] in self.children:
                return self.children[word[0]].is_prefix(word[1:])
            else:
                return False

    
class My_Trie:
    __slots__ = ('start', 'size')


    def __init__(self):
        self.start = Node("")
        self.size = 0


    def insert(self, word):
        cur_node = self.start

        for letter in word:
            if letter in cur_node.children:
                cur_node = cur_node.children[letter]
            else:
                next_node = Node(letter)
                cur_node.children[letter] = next_node
                cur_node = next_node

        cur_node.word = True
        self.size = self.size + 1


    def is_word(self, word):
        if word == "":
            return False
        else:  
            return self.start.is_word(word)

    def is_prefix(self, word):
        if word == "":
            return True
        else:
            return self.start.is_prefix(word)



trie = My_Trie()
# trie.insert("test")
# trie.insert("different")
# trie.insert("lengths")
# trie.insert("of")
# trie.insert("words")
# trie.insert("testing")
# trie.insert("test")


# while(True):
#     word = input("Prefix: ")
#     print(trie.is_prefix(word))

with open("ospd.txt", "r") as file:
    word_list = file.readlines()

    for word in word_list:
        word = word.strip()
        trie.insert(word)

