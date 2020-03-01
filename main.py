from entry import Entry
from trie import Trie
from matcher import closest_match
from utility import load_file


def on_initialize():
    print(' Command Line Dictionary by Yunhao Qian '.center(80, '='))
    print('\nStarting...\n')
    global dictionary
    dictionary = Trie()
    try:
        file = open('.dicrc')
    except:
        return
    for line in file:
        parse_line(line)
    file.close()


def on_load(arguments):
    if len(arguments) == 0:
        print('Missing argument: file names expected')
        return
    for i in range(len(arguments)):
        load_file(dictionary, arguments[i])


def hint_similar(word):
    match = closest_match(dictionary, word)
    if match != None:
        print('Did you mean: {}'.format(match))


def on_search(arguments):
    if len(arguments) == 0:
        print('Missing argument: word expected')
        return
    case_sensitive = -1
    if arguments[0].startswith('/'):
        parameter = arguments.pop(0)
        if parameter == '/c':
            case_sensitive = 0
        elif parameter == '/C':
            case_sensitive = 1
        else:
            print('Invalid parameter: {}'.format(parameter))
    if len(arguments) == 0:
        print('Missing argument: word expected')
        return
    word = ' '.join(arguments)
    entries = dictionary.find(word, case_sensitive)
    if len(entries) == 0:
        print('Found no entry for "{}"'.format(word))
        hint_similar(word)
        return
    for entry in entries:
        print(entry)
        print()


def confirm(message):
    s = input('{} (Y/N): '.format(message)).strip()
    lower = s.lower()
    if len(lower) == 0 or lower.startswith('y'):
        return True
    if not lower.startswith('n'):
        print('Invalid input: {}'.format(s))
    return False


def on_insert(arguments):
    if len(arguments) == 0:
        print('Missing argument: headword expected')
        return
    entry = Entry.create_command_line(' '.join(arguments))
    print('The following entry will be inserted:')
    print('{}\n'.format(entry))
    if confirm('Want to insert?'):
        dictionary.insert(entry)
    else:
        print('Do nothing')


def on_delete(arguments):
    if len(arguments) == 0:
        print('Missing argument: word expected')
        return
    case_sensitive = -1
    force = False
    if arguments[0].startswith('/'):
        parameter = arguments.pop(0)
        if parameter.lower() not in ['/c', '/f', '/cf', '/fc']:
            print('Invalid parameter: {}'.format(parameter))
        if 'c' in parameter:
            case_sensitive = 0
        elif 'C' in parameter:
            case_sensitive = 1
        if 'f' in parameter or 'F' in parameter:
            force = True
    if len(arguments) == 0:
        print('Missing argument: word expected')
        return
    word = ' '.join(arguments)
    entries = dictionary.find(word, case_sensitive)
    if len(entries) == 0:
        print('Found no entry for "{}"'.format(word))
        hint_similar(word)
        return
    if force:
        dictionary.erase(word, case_sensitive)
        return
    print('The following entry(ies) will be deleted:')
    for entry in entries:
        print(entry)
        print()
    if confirm('Want to delete?'):
        dictionary.erase(word, case_sensitive)
    else:
        print('Do nothing')


def on_neighbour(arguments):
    if len(arguments) == 0:
        print('Missing argument: word expected')
        return
    radius = 5
    if arguments[0].startswith('/'):
        parameter = arguments.pop(0)
        try:
            radius = int(parameter[1:])
        except:
            print('Invalid parameter: {}'.format(parameter))
        if radius <= 0:
            print('Invalid searching radius: {}'.format(radius))
            radius = 5
    if len(arguments) == 0:
        print('Missing argument: word expected')
        return
    word = ' '.join(arguments)
    if len(dictionary.find(word, 0)) == 0:
        print('Found no entry for {}'.format(word))
        hint_similar(word)
        return
    word_list = [word]
    for _ in range(radius):
        predecessor = dictionary.predecessor(word_list[0])
        if predecessor == None:
            break
        word_list.insert(0, predecessor)
    for _ in range(radius):
        successor = dictionary.successor(word_list[-1])
        if successor == None:
            break
        word_list.append(successor)
    word_list[word_list.index(word)] = '[{}]'.format(word.lower())
    for word in word_list:
        print(word)


def on_prefix(arguments):
    if len(arguments) == 0:
        print('Missing argument: prefix expected')
        return
    limit = 50
    if arguments[0].startswith('/'):
        parameter = arguments.pop(0)
        try:
            limit = int(parameter[1:])
        except:
            print('Invalid parameter: {}'.format(parameter))
        if limit <= 0:
            print('Invalid limit value: {}'.format(limit))
            limit = 50
    if len(arguments) == 0:
        print('Missing argument: prefix expected')
        return
    prefix = ' '.join(arguments)
    i = 0
    for word in dictionary.match_prefix(prefix):
        print(word)
        i += 1
        if i >= limit:
            break
    if i == 0:
        print('Found no entry with prefix "{}"'.format(prefix))


def on_match(arguments):
    if len(arguments) == 0:
        print('Missing argument: pattern expected')
        return
    tolerance = -1
    if arguments[0].startswith('/'):
        parameter = arguments.pop(0)
        try:
            tolerance = int(parameter[1:])
        except:
            print('Invalid parameter: {}'.format(parameter))
    if len(arguments) == 0:
        print('Missing argument: pattern expected')
        return
    pattern = ' '.join(arguments)
    result = closest_match(dictionary, pattern, tolerance)
    if result == None:
        print('Found no entry similar to "{}"'.format(pattern))
    else:
        print(result)


def on_size(arguments):
    if len(arguments) > 0:
        print('Redundant argument(s): {}'.format(' '.join(arguments)))
    print('Dictionary size: {}'.format(dictionary.size))


def on_save(arguments):
    if len(arguments) == 0:
        print('Missing argument: file name expected')
        print('Do nothing')
        return
    file_name = arguments.pop(0)
    if len(arguments) > 0:
        print('Redundant argument(s): {}'.format(' '.join(arguments)))
    dictionary.write_file(file_name)


def on_exit(arguments):
    if len(arguments) > 0 and arguments[0].startswith('/'):
        parameter = arguments.pop(0)
        if parameter in ['/f', '/F']:
            return False
        else:
            print('Invalid parameter: {}'.format(parameter))
    if len(arguments) > 0:
        print('Redundant argument(s): {}'.format(' '.join(arguments)))
    return not confirm('Are you sure you want to exit?')


def on_cleanup():
    print('\nExiting...')


def parse_line(line):
    arguments = line.split()
    if len(arguments) == 0:
        return True
    leading = arguments.pop(0)
    lower = leading.lower()
    if lower == 'load':
        on_load(arguments)
    elif lower == 'search':
        on_search(arguments)
    elif lower == 'insert':
        on_insert(arguments)
    elif lower == 'delete':
        on_delete(arguments)
    elif lower == 'neighbour':
        on_neighbour(arguments)
    elif lower == 'prefix':
        on_prefix(arguments)
    elif lower == 'match':
        on_match(arguments)
    elif lower == 'size':
        on_size(arguments)
    elif lower == 'save':
        on_save(arguments)
    elif lower == 'exit':
        return on_exit(arguments)
    else:
        print('Invalid argument: {}'.format(leading))
    return True


if __name__ == '__main__':
    on_initialize()
    try:
        while True:
            line = input('>>> ')
            if not parse_line(line):
                break
    except:
        print('\nThe program crashed for unknown reason')
    on_cleanup()
