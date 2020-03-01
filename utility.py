from entry import Entry
from trie import Trie


def default_file_names():
    path = 'C:/Users/yunha/Desktop/ESC190/engsci-press-python/Dictionary-in-csv'
    file_names = []
    for i in range(ord('A'), ord('Z') + 1):
        file_names.append('{}/{}.csv'.format(path, chr(i)))
    return tuple(file_names)


def load_file(dictionary, file_name):
    try:
        file = open(file_name)
    except:
        print('Failed to open file: {}'.format(file_name))
        return
    for line in file:
        line = line.strip()
        if len(line) == 0:
            continue
        try:
            dictionary.insert(Entry(line))
        except:
            print('Failed to parse the following line in file {}:\n{}'
                  .format(file_name, line))
    file.close()


def build_dictionary(file_names=None):
    if file_names == None:
        file_names = default_file_names()
    dictionary = Trie()
    for file_name in file_names:
        load_file(dictionary, file_name)
    return dictionary
