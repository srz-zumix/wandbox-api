import os
import re
import sys
import toml

from argparse import ArgumentParser
from .runner import Runner
from .cli import CLI


class RustRunner(Runner):

    MOD_REGEX = re.compile(r'^\s*mod\s+(.*?);\s*$')

    def reset(self):
        self.modules = []

    def make_code(self, file, filepath, filename):
        files = dict()
        code = ''
        for line in file:
            m = self.MOD_REGEX.match(line)
            if m:
                files.update(self.mod(os.path.dirname(filepath), m.group(1)))
            code += line
        files[filename] = code
        return files

    def mod(self, path, module_name_):
        files = dict()
        module_name = os.path.normpath(module_name_)
        if module_name in self.modules:
            return files
        module_file = module_name + '.rs'
        module_path = os.path.normpath(os.path.join(path, module_file))
        if os.path.exists(module_path):
            self.modules.append(module_name)
            files.update(self.open_code(module_path, module_file))
        return files


class RustCLI(CLI):

    def __init__(self, compiler=None):
        super(RustCLI, self).__init__('Rust', compiler, False)

    def get_runner(self, args, options):
        return RustRunner(args.language, args.compiler, args.save, args.encoding, args.retry, args.retry_wait)


class CargoCLI:

    class InnerCLI(RustCLI):

        def __init__(self, compiler=None):
            super(CargoCLI.InnerCLI, self).__init__(compiler)

        def get_runner(self, args, options):
            runner = super(CargoCLI.InnerCLI, self).get_runner(args, options)
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
        self.parser.add_argument(
            '-q',
            '--quiet',
            action='store_true',
            help='No output printed to stdout'
        )
        self.parser.add_argument(
            '-v',
            '--verbose',
            action='store_true',
            help='Use verbose output'
        )
        self.parser.add_argument(
            '--explain',
            metavar='CODE',
            action='append',
            default=[],
            help='Run `rustc --explain CODE`'
        )

        subparser = self.parser.add_subparsers()
        run_cmd = subparser.add_parser(
            'run',
            aliases=['r'],
            description='Run a binary or example of the local package',
            help='Run a binary or example of the local package. see `run -h`'
        )
        build_cmd = subparser.add_parser(
            'build',
            aliases=['b'],
            description='Run a binary or example of the local package (run command alias)',
            help='Run a binary or example of the local package (run command alias). see `build -h`'
        )
        check_cmd = subparser.add_parser(
            'check',
            aliases=['c'],
            description='Run a binary or example of the local package (run command alias)',
            help='Run a binary or example of the local package (run command alias). see `check -h`'
        )
        passthrough_cmds = [run_cmd, build_cmd, check_cmd]
        for passthrough_cmd in passthrough_cmds:
            passthrough_cmd.set_defaults(handler=self.command_run)
            passthrough_cmd.add_argument(
                '--bin',
                help='Run the specified binary.'
            )
            passthrough_cmd.add_argument(
                '--bins',
                action='store_true',
                help='Run the all binares.'
            )
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
        cmd = CargoCLI.InnerCLI(opts.compiler)
        run_options = ['run']
        cli_options = args
        if opts.dryrun:
            cli_options.append('--dryrun')
        with open('Cargo.toml', 'r') as f:
            config = toml.load(f)
            package = config['package']
            target_bin = None
            if opts.bin:
                target_bin = opts.bin
            else:
                if 'default-run' in package:
                    target_bin = package['default-run']
            for explain in opts.explain:
                run_options.append("--explain")
                run_options.append(explain)
            if opts.verbose:
                run_options.append("--verbose")
            srcs = []
            if opts.bins:
                for bin in config['bin']:
                    srcs.append(bin['path'])
            else:
                src = 'src/main.rs'
                if target_bin:
                    for bin in config['bin']:
                        if bin['name'] == target_bin:
                            src = bin['path']
                srcs.append(src)
            for src in srcs:
                exit_code = 0
                try:
                    cmd.execute_with_args(cli_options + run_options + [src])
                except SystemExit as e:
                    if e.code != 0:
                        exit_code = e.code
            sys.exit(exit_code)


def rust(compiler=None):
    cli = RustCLI(compiler)
    cli.execute()


def cargo(compiler=None):
    cli = CargoCLI(compiler)
    cli.execute()


def main():
    rust()


if __name__ == '__main__':
    main()
