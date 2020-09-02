import os
import sys
from io import StringIO

from .cli import CLI
from .runner import Runner


class ElixirCLI(CLI):

    def __init__(self, compiler=None):
        super(ElixirCLI, self).__init__('Elixir', compiler, False, False)


class ElixirMixRunner(Runner):

    def make_code(self, file, filepath, filename):
        files = super(ElixirMixRunner, self).make_code(file, filepath, filename)
        if filename != '-':
            return files
        files.update(self.open_dir('./', './'))
        return files

    def open_dir(self, dirpath, dirname):
        files = dict()
        if os.path.exists(dirname):
            for f in os.listdir(dirname):
                path = os.path.join(dirname, f)
                if os.path.isdir(path):
                    package_codes = self.open_dir(path, path)
                    files.update(package_codes)
                elif os.path.isfile(path):
                    name, ext = os.path.splitext(path)
                    if ext not in ['.exs', '.ex']:
                        continue
                    package_codes = self.open_code(path, path)
                    files.update(package_codes)
        return files


class ElixirMixCLI(CLI):

    def __init__(self, compiler=None):
        super(ElixirMixCLI, self).__init__('Elixir', compiler, False, False)

    def get_runner(self, args, options):
        return ElixirMixRunner('Bash', 'bash', args.save, args.encoding, args.retry, args.retry_wait)

    def setup_runner(self, args, enable_options, disable_options, runner):

        shell = '''
#!/bin/bash

export LC_ALL=en_US.UTF-8
export PATH=/opt/wandbox/{}/bin:$PATH
ERLANG=`cat /opt/wandbox/{}/bin/run-elixir.sh | grep -oe 'erlang-[0-9\\.]*'`
export PATH=/opt/wandbox/$ERLANG/bin:$PATH

{} || echo Unsolved: \"erts_mmap: Failed to create super carrier of size 1024 MB\", Please tell me the solution.
        '''
        command = 'mix ' + ' '.join(args.sources + args.compile_options)
        code = StringIO(shell.format(args.compiler, args.compiler, command))
        sys.stdin = code

        args.sources[:] = ['-']
        args.compile_options[:] = []

        super(ElixirMixCLI, self).setup_runner(args, enable_options, disable_options, runner)


def elixir(compiler=None):
    cli = ElixirCLI(compiler)
    cli.execute()


def mix(compiler=None):
    cli = ElixirMixCLI(compiler)
    cli.execute()


def main():
    elixir()


if __name__ == '__main__':
    main()
