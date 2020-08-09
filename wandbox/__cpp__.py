import re
import os

from .cli import CLI
from .__cxx__ import CxxRunner

class CppCLI(CLI):

    def __init__(self, compiler=None):
        super(CppCLI, self).__init__('CPP', compiler, False)
        self.cxx_setup('CPP', compiler)

    def cxx_setup(self, lang, compiler):
        self.parser.add_argument(
            '--boost',
            metavar='VERSION',
            help='set boost options version X.XX or nothing'
        )
        self.parser.add_argument(
            '--cpp-p',
            action='store_true',
            help='use cpp -P'
        )

    def get_runner(self, args, options):
        return CxxRunner(args.language, args.compiler, args.save, args.encoding, args.retry, args.retry_wait, False)

    def setup_runner(self, args, enable_options, disable_options, runner):

        def check_option(args, name):
            if hasattr(args, name):
                if getattr(args, name):
                    enable_options.append(name)
                else:
                    disable_options.append(name)
        check_option(args, 'cpp-p')
        if args.boost:
            if args.compiler not in args.boost:
                args.boost = args.boost + '-' + args.compiler
            enable_options = list(filter(lambda s: s.find('boost') == -1, enable_options))
            enable_options.append('boost-' + str(args.boost))

        super(CppCLI, self).setup_runner(args, list(set(enable_options)), disable_options, runner)


def cpp(compiler=None):
    cli = CppCLI(compiler)
    cli.execute()


def main():
    cpp()


def gcc():
    cpp('gcc-head-pp')


def clang():
    cpp('clang-head-pp')


if __name__ == '__main__':
    main()
