class Matcher:

    __slots__ = 'pattern', 'distances'

    def __init__(self, pattern):
        self.pattern = pattern
        self.distances = None

    def push_letter(self, letter):
        distances = [self.distances[-1][0] + 1]
        for i in range(1, len(self.pattern) + 1):
            d1 = distances[-1] + 1
            d2 = self.distances[-1][i] + 1
            d3 = self.distances[-1][i - 1] + int(letter != self.pattern[i - 1])
            distances.append(min(d1, d2, d3))
        self.distances.append(distances)

    def match_node(self, node, edit_distance):
        if min(self.distances[-1]) > edit_distance:
            self.distances.pop()
            return
        if self.distances[-1][-1] == edit_distance and len(node.entries) > 0:
            yield node.get_word()
        for key in node.keys:
            self.push_letter(key)
            yield from self.match_node(node.children[key], edit_distance)
        self.distances.pop()

    def match(self, trie, edit_distance):
        self.distances = [list(range(len(self.pattern) + 1))]
        yield from self.match_node(trie.root, edit_distance)


def fuzzy_match(trie, pattern, tolerance):
    matcher = Matcher(pattern)
    for edit_distance in range(tolerance + 1):
        yield from matcher.match(trie, edit_distance)


def closest_match(trie, pattern, tolerance=-1):
    if tolerance < 0:
        tolerance = len(pattern)
    for word in fuzzy_match(trie, pattern, tolerance):
        return word
    return None
