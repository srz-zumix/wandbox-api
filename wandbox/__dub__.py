import os

from .cli import CLI
from argparse import ArgumentParser


class DubCLI:

    class InnerCLI(CLI):

        def __init__(self, compiler=None):
            super(DubCLI.InnerCLI, self).__init__('D', compiler, False)

        def setup_runner(self, args, enable_options, disable_options, runner):
            super(DubCLI.InnerCLI, self).setup_runner(args, list(set(enable_options)), disable_options, runner)

    def __init__(self, compiler):
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
        passthrough_cmds = [run_cmd]
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
        cmd = DubCLI.InnerCLI(opts.compiler)
        run_options = ['run']
        cli_options = args
        if opts.dryrun:
            cli_options.append('--dryrun')
        dirname = './source'
        if os.path.exists(dirname):
            for f in os.listdir(dirname):
                path = os.path.join(dirname, f)
                name, ext = os.path.splitext(f)
                if os.path.isfile(path) and ext == '.d':
                    run_options.append(path)

        cmd.execute_with_args(cli_options + run_options)


def dub(compiler=None):
    cli = DubCLI(compiler)
    cli.execute()


def main():
    dub()


if __name__ == '__main__':
    main()
