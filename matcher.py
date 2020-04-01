class Matcher:

    __slots__ = 'pattern', 'distances'

    def __init__(self, pattern):
        self.pattern = pattern.lower()
        self.distances = [[i for i in range(len(pattern) + 1)]]

    def push_letter(self, letter):
        row = [self.distances[-1][0] + 1]
        for i in range(1, len(self.pattern) + 1):
            d1 = row[-1] + 1
            d2 = self.distances[-1][i] + 1
            d3 = self.distances[-1][i - 1] + (letter != self.pattern[i - 1])
            row.append(min(d1, d2, d3))
        self.distances.append(row)

    def match_node(self, node, edit_distance):
        if min(self.distances[-1]) > edit_distance:
            return
        if self.distances[-1][-1] == edit_distance and len(node.entries) > 0:
            yield node.get_lower_word()
        for key in node.child_keys:
            self.push_letter(key)
            yield from self.match_node(node.children[key], edit_distance)
            self.distances.pop()


def fuzzy_match(trie, pattern, tolerance):
    if tolerance < 0:
        tolerance = len(pattern)
    matcher = Matcher(pattern)
    for edit_distance in range(tolerance + 1):
        yield from matcher.match_node(trie.root, edit_distance)
