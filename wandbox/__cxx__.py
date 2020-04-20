import re
import os

from .cli import CLI
from .runner import Runner

class CxxRunner(Runner):

    EXPAND_INCLUDE_REGEX = re.compile(r'^\s*#\s*include\s*"(.*?)"')
    expand = False
    includes = []

    def make_code(self, filepath, filename):
        files = dict()
        code = ''
        file = self.file_open(filepath, 'r')
        for line in file:
            m = self.EXPAND_INCLUDE_REGEX.match(line)
            if m:
                include_filename = m.group(1)
                include_path = os.path.normpath(os.path.join(os.path.dirname(filepath), include_filename))
                if os.path.exists(include_path):
                    if self.expand:
                        expand_include_file_codes = self.open_code(include_path, include_path)
                        for c in expand_include_file_codes.values():
                            code += c
                        code += '//origin>> '
                    else:
                        include_abspath = os.path.abspath(include_path)
                        if include_abspath not in self.includes:
                            self.includes.append(include_abspath)
                            expand_include_file_codes = self.open_code(include_path, include_path)
                            files.update(expand_include_file_codes)
            code += line
        file.close()
        files[filename] = code
        return files


class CxxCLI(CLI):

    def __init__(self, compiler=None):
        super(CxxCLI, self).__init__('C++', compiler)

    def setup(self, lang, compiler):
        super(CxxCLI, self).setup(lang, compiler)
        self.parser.add_argument(
            '--std',
            metavar='VERSION',
            help='set --std options'
        )
        self.parser.add_argument(
            '--boost',
            metavar='VERSION',
            help='set boost options version X.XX or nothing'
        )
        self.parser.add_argument(
            '--optimize',
            action='store_true',
            help='use optimization'
        )
        self.parser.add_argument(
            '--cpp-verbose',
            action='store_true',
            help='use cpp-verbose'
        )
        self.parser.add_argument(
            '--sprout',
            action='store_true',
            help='use sprout'
        )
        self.parser.add_argument(
            '--msgpack',
            action='store_true',
            help='use msgpack'
        )

    def get_runner(self, args, options):
        return CxxRunner(args.language, args.compiler, args.save, args.encoding, args.retry, args.retry_wait)

    def setup_runner(self, args, enable_options, disable_options, runner):
        def filterout_cppver(opt):
            tmp = list(filter(lambda s: s.find('c++') == -1, opt))
            tmp = list(filter(lambda s: s.find('gnu++') == -1, tmp))
            return tmp
        def check_option(args, name):
            if hasattr(args, name):
                if getattr(args, name):
                    enable_options.append(name)
                else:
                    disable_options.append(name)
        check_option(args, 'cpp-verbose')
        check_option(args, 'msgpack')
        check_option(args, 'optimize')
        check_option(args, 'sprout')
        if args.boost:
            if args.compiler not in args.boost:
                args.boost = args.boost + '-' + args.compiler
            enable_options = list(filter(lambda s: s.find('boost') == -1, enable_options))
            enable_options.append('boost-' + str(args.boost))
        if args.std:
            enable_options = filterout_cppver(enable_options)
            enable_options.append(args.std)

        super(CxxCLI, self).setup_runner(args, list(set(enable_options)), disable_options, runner)


def cxx(compiler=None):
    cli = CxxCLI(compiler)
    cli.exec()


def main():
    cxx()


def gcc():
    cxx('gcc-head')


def clang():
    cxx('clang-head')


if __name__ == '__main__':
    main()
