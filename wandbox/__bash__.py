import re
import os

from argparse import ArgumentParser

from .cli import CLI
from .runner import Runner


class BashRunner(Runner):

    SOURCE_REGEX = re.compile(r'^\s*(source|\.)\s+(.*?)$')
    SHELL_REGEX = re.compile(r'^\s*(\${SHELL}|sh|bash)\s+(.*?)$')

    def reset(self):
        self.sources = []

    def make_code(self, file, filepath, filename):
        files = dict()
        code = ''
        for line in file:
            m = self.SOURCE_REGEX.match(line)
            if m:
                sourcename = m.group(2).strip('\'"')
                files.update(self.source(os.path.dirname(filepath), sourcename.strip()))
            m = self.SHELL_REGEX.match(line)
            if m:
                sourcename = m.group(2).strip('\'"')
                files.update(self.source(os.path.dirname(filepath), sourcename.strip()))
            line = line.replace('${SHELL}', '/bin/bash')
            code += line
        files[filename] = code
        return files

    def source(self, path, sname_):
        files = dict()
        sname = os.path.normpath(sname_)
        if sname in self.sources:
            return files
        file_path = os.path.normpath(os.path.join(path, sname))
        if os.path.exists(file_path):
            self.sources.append(sname)
            files.update(self.open_code(file_path, sname))
        return files


class BashCLI:

    class InnerCLI(CLI):

        def __init__(self):
            self.output = None
            super(BashCLI.InnerCLI, self).__init__('Bash', 'bash', False, False)

        def get_runner(self, args, options):
            return BashRunner(args.language, args.compiler, args.save, args.encoding, args.retry, args.retry_wait)

    def __init__(self):
        self.setup()

    # command line option
    def setup(self):
        self.parser = ArgumentParser(add_help=False)
        self.parser.add_argument(
            '-n',
            '--dryrun',
            action='store_true',
            help='dryrun'
        )

    def parse_command_line(self, argv):
        return self.parser.parse_known_args(argv)

    def execute(self):
        self.execute_with_args()

    def execute_with_args(self, args=None):
        opts, args = self.parse_command_line(args)
        cmd = BashCLI.InnerCLI()
        run_options = ['run'] + args
        cli_options = []
        if opts.dryrun:
            cli_options.append('--dryrun')
        cmd.execute_with_args(cli_options + run_options)


def bash():
    cli = BashCLI()
    cli.execute()


def main():
    bash()


if __name__ == '__main__':
    main()
