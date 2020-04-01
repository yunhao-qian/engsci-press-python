from shlex import split


def confirm(message=None, default=True):
    if message:
        print(message, end=' ')
    if default:
        print('([y]/n)', end=' ')
    else:
        print('(y/[n])', end=' ')
    response = input().strip().lower()
    if 'yes'.startswith(response):
        return True
    if 'no'.startswith(response):
        return False
    return default


def missing_argument(expect):
    print('Missing argument: expect {}'.format(expect))


def not_supported(command, mode):
    print('Does not support command "{}" in {} mode'.format(command, mode))


def redundant_arguments(argument):
    print('Redundant arguments: ignore arguments since "{}"'.format(argument))


class InvalidSyntax(Exception):

    def __init__(self, hint, line):
        Exception.__init__(
            self, 'Cannot parse the following line: {}\n{}'.format(hint, line))


class WordNotFound(Exception):

    def __init__(self, word):
        Exception.__init__(self, 'Cannot find word: {}'.format(word))
