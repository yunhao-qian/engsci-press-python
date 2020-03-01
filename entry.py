class Entry:

    __slots__ = 'headword', 'word_class', 'definition'

    def __init__(self, line):
        line = line.strip('"')
        i_open, i_close = line.index('('), -1
        depth = 1
        for i in range(i_open + 1, len(line)):
            if line[i] == '(':
                depth += 1
            elif line[i] == ')':
                depth -= 1
                if depth <= 0:
                    i_close = i
                    break
        if i_close < 0:
            raise Exception('Unknown syntax')
        self.headword = line[:i_open].rstrip()
        self.word_class = line[i_open + 1:i_close]
        self.definition = line[i_close + 1:].lstrip()

    def __str__(self):
        return '{}\n{}\n{}'.format(
            self.headword, self.word_class, self.definition)

    def write_file(self, file):
        file.write('{} ({}) {}\n'.format(
            self.headword, self.word_class, self.definition))

    @staticmethod
    def create_command_line(headword):
        entry = Entry('{}()'.format(headword))
        entry.word_class = input('Word class: ').strip()
        entry.definition = input('Definition: ').strip()
        return entry
