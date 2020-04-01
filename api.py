from dict_entry import DictEntry
from matcher import fuzzy_match
from trie import Trie
from utility import confirm, missing_argument, not_supported, \
    redundant_arguments, WordNotFound


def script_path():
    return 'esprc.txt'


def on_preloop():
    print('Starting...')
    global trie
    trie = Trie()


def on_postloop():
    print('Exiting...')


def on_load(args, interactive):
    if len(args) == 0:
        missing_argument('file name')
        return
    if len(args) > 1:
        redundant_arguments(args[1])
    try:
        trie.load(args[0])
    except OSError:
        print('Cannot open file: {}'.format(args[0]))


def on_search(args, interactive):
    if not interactive:
        not_supported('search', 'script')
        return
    case_sensitive = None
    while len(args) > 0 and args[0].startswith('--'):
        flag = args.pop(0)
        if flag == '--c':
            case_sensitive = False
        elif flag == '--C':
            case_sensitive = True
        else:
            print('Unknown flag: {}'.format(flag))
    if len(args) == 0:
        missing_argument('word')
        return
    if len(args) > 1:
        redundant_arguments(args[1])
    if case_sensitive == None:
        case_sensitive = not args[0].islower()
    entries = trie.search(args[0], case_sensitive)
    if len(entries) == 0:
        print('Find no entry named: {}'.format(args[0]))
    else:
        for entry in entries:
            print(entry)
            print()


def on_insert(args, interactive):
    if not interactive:
        not_supported('insert', 'script')
        return
    if len(args) == 0:
        missing_argument('headword')
        return
    if len(args) > 1:
        redundant_arguments(args[1])
    entry = DictEntry.from_input(args[0])
    if entry == None:
        return
    trie.insert(entry)


def on_remove(args, interactive):
    force = not interactive
    case_sensitive = None
    while len(args) > 0 and args[0].startswith('--'):
        flag = args.pop(0)
        if flag == '--f':
            force = True
        elif flag == '--c':
            case_sensitive = False
        elif flag == '--C':
            case_sensitive = True
        else:
            print('Unknown flag: {}'.format(flag))
    if len(args) == 0:
        missing_argument('word')
        return
    if len(args) > 1:
        redundant_arguments(args[1])
    if case_sensitive == None:
        case_sensitive = not args[0].islower()
    if force:
        trie.remove(args[0], case_sensitive)
        return
    entries = trie.search(args[0], case_sensitive)
    if len(entries) == 0:
        print('Find no entry named: {}'.format(args[0]))
        return
    print('Will remove the following entries:')
    for entry in entries:
        print(entry)
        print()
    if not confirm('Continue?'):
        return
    trie.remove(args[0], case_sensitive)


def on_neighbor(args, interactive):
    if not interactive:
        not_supported('neighbor', 'script')
        return
    radius = 5
    while len(args) > 0 and args[0].startswith('--'):
        flag = args.pop(0)[2:]
        valid = True
        if flag == '':
            valid = False
        else:
            try:
                number = int(flag)
            except ValueError:
                valid = False
            else:
                if number < 0:
                    print('Radius out of range: {}'.format(number))
                else:
                    radius = number
        if not valid:
            print('Unknown flag: --{}'.format(flag))
    if len(args) == 0:
        missing_argument('word')
        return
    if len(args) > 1:
        redundant_arguments(args[1])
    try:
        predecessors, successors = trie.get_neighbors(args[0], radius)
    except WordNotFound as exception:
        print(exception)
        return
    for i in range(len(predecessors) - 1, -1, -1):
        print(predecessors[i])
    print('[{}]'.format(args[0].lower()))
    for successor in successors:
        print(successor)


def on_prefix(args, interactive):
    if not interactive:
        not_supported('prefix', 'script')
        return
    if not interactive:
        not_supported('search', 'script')
        return
    case_sensitive = None
    while len(args) > 0 and args[0].startswith('--'):
        flag = args.pop(0)
        if flag == '--c':
            case_sensitive = False
        elif flag == '--C':
            case_sensitive = True
        else:
            print('Unknown flag: {}'.format(flag))
    if len(args) == 0:
        missing_argument('word')
        return
    if len(args) > 1:
        redundant_arguments(args[1])
    if case_sensitive == None:
        case_sensitive = not args[0].islower()
    i = 0
    for word in trie.match_prefix(args[0], case_sensitive):
        if i >= 50:
            break
        print(word)
        i += 1
    if i == 0:
        print('Find no word starting with: {}'.format(args[0]))


def on_match(args, interactive):
    if not interactive:
        not_supported('match', 'script')
        return
    tolerance = -1
    while len(args) > 0 and args[0].startswith('--'):
        flag = args.pop(0)[2:]
        valid = True
        if flag == '':
            valid = False
        else:
            try:
                number = int(flag)
            except ValueError:
                valid = False
            else:
                if number < 0:
                    print('Tolerance out of range: {}'.format(number))
                else:
                    tolerance = number
        if not valid:
            print('Unknown flag: --{}'.format(flag))
    if len(args) == 0:
        missing_argument('pattern')
        return
    if len(args) > 1:
        redundant_arguments(args[1])
    i = 0
    for word in fuzzy_match(trie, args[0], tolerance):
        if i >= 5:
            break
        print(word)
        i += 1
    if i == 0:
        print('Find no word similar to: {}'.format(args[0]))


def on_size(args, interactive):
    if not interactive:
        not_supported('size', 'script')
        return
    while len(args) > 0 and args[0].startswith('--'):
        print('Unknown flag: {}'.format(args.pop(0)))
    if len(args) > 0:
        redundant_arguments(args[0])
    print('Size of dictionary: {}'.format(trie.size))


def on_write(args, interactive):
    force = not interactive
    while len(args) > 0 and args[0].startswith('--'):
        flag = args.pop(0)
        if flag == '--f':
            force = True
        else:
            print('Unknown flag: {}'.format(flag))
    if len(args) > 1:
        redundant_arguments(args[1])
    if trie.size == 0 and not force:
        if not confirm("Dictionary is empty. Continue?", False):
            return
    try:
        trie.write(args[0])
    except OSError:
        print('Cannot open file: {}'.format(args[0]))


def on_exit(args, interactive):
    if not interactive:
        not_supported('exit', 'script')
        return False
    force = False
    while len(args) > 0 and args[0].startswith('--'):
        flag = args.pop(0)
        if flag == '--f':
            force = True
        else:
            print('Unknown flag: {}'.format(flag))
    if len(args) > 0:
        redundant_arguments(args[0])
    if force:
        return True
    return confirm('Are you sure you want to exit?')
