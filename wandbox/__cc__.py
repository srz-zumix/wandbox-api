from .cli import CLI
from .__cxx__ import CxxRunner


class CcCLI(CLI):

    def __init__(self, compiler=None):
        super(CcCLI, self).__init__('C', compiler)
        self.cxx_setup('C', compiler)

    def cxx_setup(self, lang, compiler):
        self.parser.add_argument(
            '--std',
            metavar='VERSION',
            help='set --std options'
        )
        self.parser.add_argument(
            '--no-warning',
            action='store_true',
            help='disable warning option'
        )
        self.parser.add_argument(
            '--optimize',
            action='store_true',
            help='use optimization'
        )
        self.parser.add_argument(
            '--cpp-pedantic',
            metavar='PEDANTIC',
            help='use cpp-pedantic'
        )
        self.parser.add_argument(
            '--cpp-verbose',
            action='store_true',
            help='use cpp-verbose'
        )

    def get_runner(self, args, options):
        return CxxRunner(args.language, args.compiler, args.save, args.encoding, args.retry, args.retry_wait)

    def setup_runner(self, args, enable_options, disable_options, runner):

        def filterout_cppver(opt):
            tmp = list(filter(lambda s: s.find('c') == -1, opt))
            tmp = list(filter(lambda s: s.find('gnu') == -1, tmp))
            return tmp

        self.check_bool_option(args, 'no-warning'   , enable_options, disable_options)
        self.check_bool_option(args, 'cpp-verbose'  , enable_options, disable_options)
        self.check_bool_option(args, 'optimize'     , enable_options, disable_options)
        if args.cpp_pedantic:
            pedantic_opt = args.cpp_pedantic
            if args.cpp_pedantic == 'no':
                pedantic_opt = 'cpp-no-pedantic'
            elif args.cpp_pedantic == 'yes':
                pedantic_opt = 'cpp-pedantic'
            elif args.cpp_pedantic == 'error':
                pedantic_opt = 'cpp-pedantic-errors'
            elif args.cpp_pedantic == 'errors':
                pedantic_opt = 'cpp-pedantic-errors'
            enable_options = list(filter(lambda s: s.find('pedantic') == -1, enable_options))
            enable_options.append(pedantic_opt)
        if args.std:
            enable_options = filterout_cppver(enable_options)
            enable_options.append(args.std)

        super(CcCLI, self).setup_runner(args, list(set(enable_options)), disable_options, runner)


def cc(compiler=None):
    cli = CcCLI(compiler)
    cli.execute()


def main():
    cc()


def gcc():
    cc('gcc-*-c')


def clang():
    cc('clang-*-c')


if __name__ == '__main__':
    main()
