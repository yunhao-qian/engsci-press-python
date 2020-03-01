class TrieNode:

    __slots__ = 'letter', 'entries', 'parent', 'children', 'keys'

    def __init__(self, letter, parent):
        self.letter = letter
        self.entries = []
        self.parent = parent
        self.children = {}
        self.keys = []

    def is_leaf(self):
        return self.parent != None and len(self.keys) == 0

    def get_word(self):
        word = ''
        node = self
        while node != None and node.letter != None:
            word = node.letter + word
            node = node.parent
        return word

    def insert_child(self, letter):
        self.keys.append(letter)
        self.keys.sort()
        self.children[letter] = TrieNode(letter, self)

    def erase_child(self, letter):
        del self.keys[self.keys.index(letter)]
        del self.children[letter]


class Trie:

    __slots__ = 'root', 'size'

    def __init__(self):
        self.root = TrieNode(None, None)
        self.size = 0

    def __len__(self):
        return self.size

    def get_node(self, word):
        node = self.root
        for letter in word.lower():
            if letter not in node.keys:
                return None
            node = node.children[letter]
        return node

    def find(self, word, case_sensitive=0):
        if case_sensitive == 0:
            case_sensitive = False
        elif case_sensitive > 0:
            case_sensitive = True
        else:
            case_sensitive = not word.islower()
        node = self.get_node(word)
        if node == None or len(node.entries) == 0:
            return ()
        if not case_sensitive:
            return tuple(node.entries)
        entries = []
        for entry in node.entries:
            if entry.headword == word:
                entries.append(entry)
        return tuple(entries)

    def insert(self, entry):
        node = self.root
        for letter in entry.headword.lower():
            if letter not in node.keys:
                node.insert_child(letter)
            node = node.children[letter]
        node.entries.append(entry)
        self.size += 1

    def erase(self, word, case_sensitive=0):
        if case_sensitive == 0:
            case_sensitive = False
        elif case_sensitive > 0:
            case_sensitive = True
        else:
            case_sensitive = not word.islower()
        node = self.get_node(word)
        if node == None or len(node.entries) == 0:
            return
        if not case_sensitive:
            self.size -= len(node.entries)
            node.entries = []
        else:
            i = 0
            while i < len(node.entries):
                if node.entries[i].headword == word:
                    del node.entries[i]
                    self.size -= 1
                else:
                    i += 1
        while node.is_leaf() and len(node.entries) == 0:
            letter = node.letter
            node = node.parent
            node.erase_child(letter)

    def previous_node(self, node):
        letter = node.letter
        node = node.parent
        if node == None:
            return None
        index = node.keys.index(letter)
        if index == 0:
            return node
        node = node.children[node.keys[index - 1]]
        while len(node.keys) > 0:
            node = node.children[node.keys[-1]]
        return node

    def next_node(self, node):
        if len(node.keys) > 0:
            return node.children[node.keys[0]]
        while True:
            letter = node.letter
            node = node.parent
            if node == None:
                return None
            index = node.keys.index(letter)
            if index != len(node.keys) - 1:
                return node.children[node.keys[index + 1]]

    def predecessor(self, word):
        node = self.get_node(word)
        while True:
            node = self.previous_node(node)
            if node == None:
                return None
            if len(node.entries) > 0:
                return node.get_word()

    def successor(self, word):
        node = self.get_node(word)
        while True:
            node = self.next_node(node)
            if node == None:
                return None
            if len(node.entries) > 0:
                return node.get_word()

    def keys(self, node=None):
        if node == None:
            node = self.root
        if len(node.entries) > 0:
            yield node.get_word()
        for key in node.keys:
            yield from self.keys(node.children[key])

    def values(self, node=None):
        if node == None:
            node = self.root
        for entry in node.entries:
            yield entry
        for key in node.keys:
            yield from self.values(node.children[key])

    def __iter__(self):
        return self.keys()

    def match_prefix(self, prefix):
        node = self.get_node(prefix)
        if node != None:
            yield from self.keys(node)

    def write_file(self, file_name):
        try:
            file = open(file_name, 'w')
        except:
            print('Unable to open file: {}'.format(file_name))
            return
        for value in self.values():
            value.write_file(file)
        file.close()
