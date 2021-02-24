from .cli import CLI
from .__cxx__ import CxxRunner


class CppCLI(CLI):

    def __init__(self, compiler=None):
        super(CppCLI, self).__init__('CPP', compiler)
        self.cxx_setup('CPP', compiler)

    def cxx_setup(self, lang, compiler):
        self.parser.add_argument(
            '--boost',
            metavar='VERSION',
            help='set boost options version X.XX or nothing'
        )
        self.parser.add_argument(
            '--no-cpp-p',
            action='store_true',
            help='disable cpp -P'
        )

    def get_runner(self, args, options):
        return CxxRunner(args.language, args.compiler, args.save, args.encoding, args.retry, args.retry_wait)

    def setup_runner(self, args, enable_options, disable_options, runner):

        self.check_bool_option(args, 'no-cpp-p'  , enable_options, disable_options)
        if args.boost:
            postfix = args.compiler.replace('-pp', '-header')
            if postfix not in args.boost:
                args.boost = args.boost + '-' + postfix
            enable_options = list(filter(lambda s: s.find('boost') == -1, enable_options))
            enable_options.append('boost-' + str(args.boost))

        super(CppCLI, self).setup_runner(args, list(set(enable_options)), disable_options, runner)


def cpp(compiler=None):
    cli = CppCLI(compiler)
    cli.execute()


def main():
    cpp()


def gcc():
    cpp('gcc-*-pp')


def clang():
    cpp('clang-*-pp')


if __name__ == '__main__':
    main()
