from bisect import insort
from collections import defaultdict


class TrieNode:

    __slots__ = 'letter', 'entries', 'parent', 'child_keys', 'children'

    def __init__(self, letter, parent):
        self.letter = letter
        self.entries = []
        self.parent = parent
        self.child_keys = []
        self.children = defaultdict(lambda: None)

    def get_lower_word(self):
        return self.entries[0].headword.lower()

    def insert_child(self, letter):
        insort(self.child_keys, letter)
        child = TrieNode(letter, self)
        self.children[letter] = child
        return child

    def remove_child(self, letter):
        self.child_keys.remove(letter)
        del self.children[letter]

    def previous_node(self):
        parent = self.parent
        if parent == None:
            return None
        index = parent.child_keys.index(self.letter)
        if index == 0:
            return parent
        node = parent.children[parent.child_keys[index - 1]]
        while len(node.child_keys) > 0:
            node = node.children[node.child_keys[-1]]
        return node

    def next_node(self):
        if len(self.child_keys) > 0:
            return self.children[self.child_keys[0]]
        node = self
        while True:
            letter = node.letter
            node = node.parent
            if node == None:
                return None
            index = node.child_keys.index(letter)
            if index != len(node.child_keys) - 1:
                return node.children[node.child_keys[index + 1]]

    def keys(self):
        if len(self.entries) > 0:
            yield self.get_lower_word()
        for key in self.child_keys:
            yield from self.children[key].keys()

    def values(self):
        for entry in self.entries:
            yield entry
        for key in self.child_keys:
            yield from self.children[key].values()
