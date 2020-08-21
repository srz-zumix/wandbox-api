import sys

from argparse import ArgumentParser
from argparse import SUPPRESS
from io import StringIO

from .cli import CLI


class OpenSSLCLI:

    def __init__(self):
        self.setup()

    def command_run(self, args):
        options = []
        for o in args.options:
            options.extend(o.split(','))
        try:
            self.run(args, options)
        except Exception as e:
            print(e)
            self.print_help()
            sys.exit(1)

    # command line option
    def setup(self):
        self.parser = ArgumentParser()
        self.parser.add_argument(
            '-out',
            help=SUPPRESS
        )

    def parse_command_line(self, argv):
        return self.parser.parse_known_args(argv)

    def print_help(self):
        self.parser.print_help()

    def execute(self):
        self.execute_with_args()

    def execute_with_args(self, args=None):
        opts, args = self.parse_command_line(args)
        cmd = CLI('OpenSSL', 'openssl-head')
        cmd.result_key = 'program_message'
        code = StringIO('openssl ' + ' '.join(args))
        sys.stdin = code
        cmd.execute_with_args(['run', '-'])


def main():
    cli = OpenSSLCLI()
    cli.execute()


if __name__ == '__main__':
    main()
