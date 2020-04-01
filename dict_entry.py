from utility import confirm, InvalidSyntax


class DictEntry:

    __slots__ = 'headword', 'word_class', 'definition'

    def __init__(self, headword, word_class, definition):
        self.headword = headword
        self.word_class = word_class
        self.definition = definition

    @staticmethod
    def from_line(line):
        if line.startswith('"') and line.endswith('"'):
            line = line[1:-1]
        left_index = line.index('(')
        if left_index < 0:
            raise InvalidSyntax('missing word class', line)
        right_index = -1
        depth = 1
        for i in range(left_index + 1, len(line)):
            if line[i] == '(':
                depth += 1
            elif line[i] == ')':
                depth -= 1
                if depth == 0:
                    right_index = i
                    break
        if right_index < 0:
            raise InvalidSyntax('mismatched brackets', line)
        headword = line[:left_index].strip()
        if headword == '':
            raise InvalidSyntax('empty headword', line)
        word_class = line[left_index + 1:right_index].strip()
        definition = line[right_index + 1:].strip()
        return DictEntry(headword, word_class, definition)

    @staticmethod
    def from_input(headword):
        word_class = input('Word class: ').strip()
        definition = input('Definition: ').strip()
        entry = DictEntry(headword, word_class, definition)
        print('The following entry will be created:')
        print(entry)
        if confirm("Continue?"):
            return entry
        else:
            return None

    def write(self, stream):
        stream.write('{} ({}) {}'.format(
            self.headword, self.word_class, self.definition))

    def __str__(self):
        return '{}\n{}\n{}'.format(
            self.headword, self.word_class, self.definition)
