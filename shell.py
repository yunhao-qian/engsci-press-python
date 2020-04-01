from api import *
from cmd import Cmd
from shlex import split


class Shell(Cmd):
    __slots__ = 'interactive'

    intro = '{}\n{}\n{}'.format(
        '*==============================================*'.center(80),
        '||   EngSci Press Dictionary by Yunhao Qian   ||'.center(80),
        '*==============================================*'.center(80))

    prompt = '>>> '

    def emptyline(self):
        pass

    def preloop(self):
        on_preloop()
        self.interactive = False
        try:
            stream = open(script_path(), 'r')
        except OSError:
            pass
        else:
            for line in stream:
                self.onecmd(line)
            stream.close()
        self.interactive = True

    def postloop(self):
        on_postloop()

    def do_load(self, line):
        on_load(split(line), self.interactive)

    def do_search(self, line):
        on_search(split(line), self.interactive)

    def do_insert(self, line):
        on_insert(split(line), self.interactive)

    def do_remove(self, line):
        on_remove(split(line), self.interactive)

    def do_neighbor(self, line):
        on_neighbor(split(line), self.interactive)

    def do_prefix(self, line):
        on_prefix(split(line), self.interactive)

    def do_match(self, line):
        on_match(split(line), self.interactive)

    def do_size(self, line):
        on_size(split(line), self.interactive)

    def do_write(self, line):
        on_write(split(line), self.interactive)

    def do_exit(self, line):
        return on_exit(split(line), self.interactive)


if __name__ == '__main__':
    Shell().cmdloop()
