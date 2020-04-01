from dict_entry import DictEntry
from trie_node import TrieNode
from utility import InvalidSyntax, WordNotFound


class Trie:

    __slots__ = 'root', 'size'

    def __init__(self):
        self.root = TrieNode(None, None)
        self.size = 0

    def insert(self, entry):
        node = self.root
        for letter in entry.headword.lower():
            child = node.children[letter]
            if child:
                node = child
            else:
                node = node.insert_child(letter)
        node.entries.append(entry)
        self.size += 1

    def get_node(self, word):
        node = self.root
        for letter in word.lower():
            node = node.children[letter]
            if node == None:
                return None
        return node

    def search(self, word, case_sensitive):
        node = self.get_node(word)
        if node == None or len(node.entries) == 0:
            return []
        if case_sensitive:
            entries = []
            for entry in node.entries:
                if entry.headword == word:
                    entries.append(entry)
            return entries
        else:
            return node.entries.copy()

    def remove(self, word, case_sensitive):
        node = self.get_node(word)
        if node == None or len(node.entries) == 0:
            return
        if case_sensitive:
            i = 0
            while i < len(node.entries):
                if node.entries[i].headword == word:
                    del node.entries[i]
                    self.size -= 1
                else:
                    i += 1
        else:
            self.size -= len(node.entries)
            del node.entries[:]
        while len(node.child_keys) == 0 and len(node.entries) == 0:
            letter = node.letter
            node = node.parent
            if node == None:
                break
            node.remove_child(letter)

    def get_neighbors(self, word, radius):
        node = self.get_node(word)
        if node == None:
            raise WordNotFound(word)
        predecessors = []
        count = 0
        neighbor = node.previous_node()
        while neighbor and count < radius:
            if len(neighbor.entries) > 0:
                predecessors.append(neighbor.get_lower_word())
                count += 1
            neighbor = neighbor.previous_node()
        successors = []
        count = 0
        neighbor = node.next_node()
        while neighbor and count < radius:
            if len(neighbor.entries) > 0:
                successors.append(neighbor.get_lower_word())
                count += 1
            neighbor = neighbor.next_node()
        return predecessors, successors

    def match_prefix(self, prefix, case_sensitive):
        node = self.get_node(prefix)
        if node == None:
            return
        if case_sensitive:
            yielded = set()
            for entry in node.values():
                word = entry.headword
                if word.startswith(prefix) and word not in yielded:
                    yield word
                    yielded.add(word)
        else:
            yield from node.keys()

    def load(self, file_name):
        stream = open(file_name, 'r')
        for line in stream:
            line = line.strip()
            if line == '':
                continue
            try:
                entry = DictEntry.from_line(line)
            except InvalidSyntax as exception:
                print(exception)
            else:
                self.insert(entry)
        stream.close()

    def write(self, file_name):
        stream = open(file_name, 'w')
        for entry in self.root.values():
            entry.write(stream)
        stream.close()
