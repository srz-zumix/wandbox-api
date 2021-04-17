import glob
import os
import re
import yaml

from argparse import ArgumentParser
from .runner import Runner
from .cli import CLI


class GhcRunner(Runner):

    IMPORT_REGEX = re.compile(r'^\s*import\s+(.*?)$')

    def reset(self):
        self.required = []
        self.incdirs = []

    def make_code(self, file, filepath, filename):
        files = dict()
        code = ''
        for line in file:
            m = self.IMPORT_REGEX.match(line)
            if m:
                files.update(self.on_import(m.group(1)))
            code += line
        files[filename] = code
        return files

    def set_search_path(self, paths):
        self.search_path = paths

    def add_search_path(self, path):
        self.search_path.append(path)

    def on_import(self, path):
        files = dict()
        # TODO
        return files

    def build_compiler_options(self, options):
        super(GhcRunner, self).build_compiler_options(options)
        self.add_commandline_options('-dynamic')


class GhcCLI(CLI):

    def __init__(self, compiler=None):
        super(GhcCLI, self).__init__('Haskell', compiler)

    def get_runner(self, args, options):
        return GhcRunner(args.language, args.compiler, args.save, args.encoding, args.retry, args.retry_wait)


class HaskellStackCLI:

    class InnerCLI(GhcCLI):

        def __init__(self, compiler=None):
            self.libdirs = []
            super(HaskellStackCLI.InnerCLI, self).__init__(compiler)

        def get_runner(self, args, options):
            runner = super(HaskellStackCLI.InnerCLI, self).get_runner(args, options)
            runner.set_search_path(self.libdirs)
            return runner

    def __init__(self, compiler=None):
        self.setup(compiler)

    # command line option
    def setup(self, compiler):
        self.parser = ArgumentParser(add_help=False)
        self.parser.add_argument(
            '-c',
            '--compiler',
            default=compiler
        )
        self.parser.add_argument(
            '-n',
            '--dryrun',
            action='store_true',
            help='dryrun'
        )

        subparser = self.parser.add_subparsers()
        run_cmd = subparser.add_parser(
            'run',
            prefix_chars='+',
            description='build and run command',
            help='build and run command. see `run +h`'
        )
        build_cmd = subparser.add_parser(
            'build',
            prefix_chars='+',
            description='build and run command (run command alias)',
            help='build and run command (run command alias). see `build +h`'
        )
        passthrough_cmds = [run_cmd, build_cmd]
        for passthrough_cmd in passthrough_cmds:
            passthrough_cmd.set_defaults(handler=self.command_run)
            passthrough_cmd.add_argument(
                'options',
                metavar='OPTIONS',
                nargs='*',
                help='options'
            )

    def parse_command_line(self, argv):
        opts, args = self.parser.parse_known_args(argv)
        if 'WANDBOX_DRYRUN' in os.environ:
            opts.dryrun = True
        return opts, args

    def print_help(self):
        self.parser.print_help()

    def execute(self):
        self.execute_with_args()

    def execute_with_args(self, args=None):
        opts, args = self.parse_command_line(args)
        if hasattr(opts, 'handler'):
            opts.handler(opts, args)
        else:
            self.print_help()

    def command_run(self, opts, args):
        cmd = HaskellStackCLI.InnerCLI(opts.compiler)
        run_options = ['run']
        cli_options = args
        if opts.dryrun:
            cli_options.append('--dryrun')
        with open('package.yaml', 'r') as yml:
            config = yaml.safe_load(yml)
            exec_config = config['executables']['haskell-stack-exe']
            main = exec_config['main']
            main_dir = exec_config['source-dirs']
            run_options.append(os.path.join(main_dir, main))
            options = exec_config['ghc-options']
            run_options.extend(options)

            dirs = config['library']['source-dirs']
            if isinstance(dirs, str):
                dirs = [dirs]
            for dir in dirs:
                cmd.libdirs.append(dir)
                for x in glob.glob(os.path.join(dir, '*.hs')):
                    run_options.append(x)

        cmd.execute_with_args(cli_options + run_options)


def ghc(compiler=None):
    cli = GhcCLI(compiler)
    cli.execute()


def haskell_stack(compiler=None):
    cli = HaskellStackCLI(compiler)
    cli.execute()


def main():
    ghc()


if __name__ == '__main__':
    main()
