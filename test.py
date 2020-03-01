from matcher import fuzzy_match, closest_match
from utility import build_dictionary


def test_dictionary():
    dictionary = build_dictionary()
    print(len(dictionary))
    words = [word for word in dictionary]
    print(len(words))
    for word in words:
        dictionary.erase(word)
    print(len(dictionary))


def test_tranverse_order():
    dictionary = build_dictionary()
    previous = ''
    for word in dictionary:
        if previous >= word:
            print('Wrong order: {} and {}'.format(previous, word))
        previous = word


def test_fuzzy_match():
    dictionary = build_dictionary()
    while True:
        try:
            pattern = input('\n>>> ').strip()
            tolerance = int(input('T = ').strip())
        except:
            return
        print()
        for match in fuzzy_match(dictionary, pattern, tolerance):
            print(match)


def test_find_word():
    dictionary = build_dictionary()
    while True:
        try:
            word = input('\n>>> ').strip()
        except:
            return
        entries = dictionary.find(word)
        if len(entries) > 0:
            for entry in entries:
                print('\n{}'.format(entry))
        else:
            print('\nWord not found!')
            match = closest_match(dictionary, word)
            if match != None:
                print('Did you mean: {}'.format(match))


def test_match_prefix():
    dictionary = build_dictionary()
    while True:
        try:
            prefix = input('\n>>> ').strip()
        except:
            return
        print()
        for match in dictionary.match_prefix(prefix):
            print(match)


def test_write_file():
    dictionary = build_dictionary()
    dictionary.write_file('dictionary.txt')
    new_dictionary = build_dictionary(['dictionary.txt'])
    print(dictionary.size, new_dictionary.size)


def test_predecessor_successor():
    dictionary = build_dictionary()
    while True:
        try:
            word = input('\n>>> ').strip()
        except:
            return
        predecessor = dictionary.predecessor(word)
        successor = dictionary.successor(word)
        print('\n{}\n{}\n{}'.format(predecessor, word, successor))


def test_adjacency_order():
    dictionary = build_dictionary()
    array = [word for word in dictionary]
    for i in range(len(array)):
        expected = None if i == 0 else array[i - 1]
        actual = dictionary.predecessor(array[i])
        if expected != actual:
            print('Wrong predecessor: {} and {}', expected, actual)
        expected = None if i == len(array) - 1 else array[i + 1]
        actual = dictionary.successor(array[i])
        if expected != actual:
            print('Wrong successor: {} and {}', expected, actual)


def get_max_string_length():
    dictionary = build_dictionary()
    L1, L2, L3 = 0, 0, 0
    for entry in dictionary.values():
        L1 = max(L1, len(entry.headword))
        L2 = max(L2, len(entry.word_class))
        L3 = max(L3, len(entry.definition))
    print(L1, L2, L3)


def get_ascii_range():
    alphabet = set()
    dictionary = build_dictionary()
    for value in dictionary.values():
        for letter in value.headword:
            alphabet.add(letter)
    alphabet = [ord(letter) for letter in alphabet]
    alphabet.sort()
    print(alphabet)


if __name__ == '__main__':
    # test_dictionary()
    # test_tranverse_order()
    # test_fuzzy_match()
    # test_find_word()
    # test_match_prefix()
    # test_write_file()
    # test_predecessor_successor()
    # test_adjacency_order()
    # get_max_string_length()
    get_ascii_range()
