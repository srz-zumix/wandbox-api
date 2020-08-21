import sys

from argparse import ArgumentParser
from argparse import SUPPRESS
from io import StringIO

from .cli import CLI
from .wandbox import Wandbox


class OpenSSLCLI:

    class InnerCLI(CLI):

        def __init__(self):
            self.output = None
            super(OpenSSLCLI.InnerCLI, self).__init__('OpenSSL', 'openssl-head', False)

        def on_run_response(self, response):
            if self.output:
                with open(self.output, 'w') as file:
                    if 'program_output' in response:
                        file.write(response['program_output'])
                    else:
                        file.write(response['program_message'])
            return super(OpenSSLCLI.InnerCLI, self).on_run_response(response)


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
        self.parser = ArgumentParser(add_help=False)
        self.parser.add_argument(
            '-out',
            help=SUPPRESS
        )
        self.parser.add_argument(
            '-in',
            dest='infile',
            help=SUPPRESS
        )
        self.parser.add_argument(
            'command',
            nargs='?',
            help=SUPPRESS
        )
        self.parser.add_argument(
            '-n',
            '--dryrun',
            action='store_true',
            help='dryrun'
        )

    def parse_command_line(self, argv):
        return self.parser.parse_known_args(argv)

    def print_help(self):
        self.parser.print_help()

    def execute(self):
        self.execute_with_args()

    def execute_with_args(self, args=None):
        opts, args = self.parse_command_line(args)
        cmd = OpenSSLCLI.InnerCLI()
        cmd.output = opts.out
        if cmd.output:
            cmd.result_key = 'program_error'
        else:
            cmd.result_key = 'program_message'
        run_options = ['run']
        cli_options = []
        if opts.dryrun:
            cli_options.append('--dryrun')
        sslcmd = opts.command
        sslopts = args
        if opts.infile:
            sslopts = [ '-in', opts.infile ] + sslopts
            run_options.append(opts.infile)
        command = ' '.join(['openssl', sslcmd] + sslopts)
        code = StringIO(command)
        sys.stdin = code
        run_options.append('-')
        cmd.execute_with_args(cli_options + run_options)


def main():
    cli = OpenSSLCLI()
    cli.execute()


if __name__ == '__main__':
    main()
