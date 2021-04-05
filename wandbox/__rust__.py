import os
import re
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

        subparser = self.parser.add_subparsers()
        run_cmd = subparser.add_parser(
            'run',
            description='build and run command',
            help='build and run command. see `run +h`'
        )
        run_cmd.add_argument(
            '--bin',
            help='Run the specified binary.'
        )
        build_cmd = subparser.add_parser(
            'build',
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
            src = 'src/main.rs'
            if target_bin:
                for bin in config['bin']:
                    if bin['name'] == target_bin:
                        src = bin['path']
            else:
                pass
            run_options.append(src)

        cmd.execute_with_args(cli_options + run_options)


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
