import re
import sys
from . import __version__ as VERSION

from .__all__ import get_all_cli

from .wandbox import Wandbox
from .wandbox_compile_response import WandboxCompileResponse
from .utils import text_transform
from argparse import ArgumentParser


class StatusCLI:

    def __init__(self):
        self.setup()

    # command line option
    def setup(self):
        self.parser = ArgumentParser()
        self.parser.add_argument(
            '-v',
            '--version',
            action='version',
            version=u'%(prog)s version ' + VERSION
        )
        self.parser.add_argument(
            '-l',
            '--language',
            required=True,
            help='specify language'
        )
        self.parser.add_argument(
            '-c',
            '--compiler',
            help='specify compiler (can use fnmatch, use first match compiler. e.g. clang-3.9.*[!c] => clang-3.9.1)'
        )
        self.parser.add_argument(
            '-V',
            '--verbose',
            action='store_true',
            help='verbose log'
        )

    def parse_command_line(self, argv):
        return self.parser.parse_args(argv)

    def execute(self):
        self.execute_with_args()

    def execute_with_args(self, args=None):
        opts = self.parse_command_line(args)

        language, compiler, *_ = re.split(r'[\s:,]', opts.language, 2) + [None]
        clis = get_all_cli()
        cli = next((cli for cli in clis if cli.language == language), None)

        if cli is None:
            print("error: \"{}\" language is not found".format(language))
            self.parser.print_help()
            sys.exit(1)

        if opts.compiler:
            compiler = opts.compiler

        run_options = ['run-template']
        cli_options = ['-c', compiler] if compiler else []
        StatusCLI.verbose = opts.verbose
        if opts.verbose:
            cli_options.append('-V')

        cli.on_run_response = type(cli.on_run_response)(StatusCLI.OnRunResponse, cli)
        cli.execute_with_args(cli_options + run_options)

    @staticmethod
    def OnRunResponse(cli, response):
        r = WandboxCompileResponse(response)
        if r.has_error():
            print(r.error())
            return 1
        if StatusCLI.verbose:
            Wandbox.ShowResult(response)
        if StatusCLI.CheckResponse(cli, r):
            if r.has_signal():
                print(r.signal())
            else:
                print('Compile/Runtime Error')
            return 1
        print('OK')
        return 0

    @staticmethod
    def CheckResponse(cli, r):
        if r.has_program_output():
            if not StatusCLI.CheckOutput(cli.language, text_transform(r.program_output())):
                return 1
        else:
            return 1
        if r.has_status():
            return int(r.status())
        return 0

    @staticmethod
    def CheckOutput(language, output):
        if language == "OpenSSL":
            return "PRIVATE KEY" in output
        elif language == "CPP":
            return "42" in output
        else:
            return "Hello" in output


def status():
    cli = StatusCLI()
    cli.execute()


def main():
    status()


if __name__ == '__main__':
    main()
