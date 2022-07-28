import os
import re

from .cli import CLI
from .runner import Runner


class ZigRunner(Runner):

    IMPORT_REGEX = re.compile(r'\s*=\s*@import\s*\((.*?)\)[^;]*;')
    EMBEDDED = ["root", "std", "builtin"]

    def reset(self):
        self.imports = []

    def make_code(self, file, filepath, filename):
        files = dict()
        code = ''
        for line in file:
            ml = self.IMPORT_REGEX.finditer(line)
            for m in ml:
                import_str = m.group(1).strip('\'"')
                if import_str not in self.EMBEDDED:
                    files.update(self.import_file(filepath, import_str))
            code += line
        files[filename] = code
        return files

    def import_file(self, filepath, import_str):
        files = dict()
        import_path = os.path.normpath(os.path.join(os.path.dirname(filepath), import_str))
        if os.path.exists(import_path):
            import_abspath = os.path.abspath(import_path)
            if import_abspath not in self.imports:
                self.imports.append(import_abspath)
                files.update(self.open_code(import_path, import_path))
        return files


class ZigCLI(CLI):

    def __init__(self, compiler=None):
        super(ZigCLI, self).__init__('Zig', compiler)
        self.zig_setup('Zig', compiler)

    def zig_setup(self, lang, compiler):
        self.parser.add_argument(
            '--strip',
            action='store_true',
            help='set --strip'
        )
        self.parser.add_argument(
            '--single-threaded',
            action='store_true',
            help='set -fsingle-threaded'
        )
        self.parser.add_argument(
            '--std-cxx',
            choices=['Debug', 'ReleaseSafe', 'ReleaseSmall', 'ReleaseFast'],
            default='ReleaseSafe',
            help='set -O'
        )

    def get_runner(self, args, options):
        return ZigRunner(args.language, args.compiler, args.save, args.encoding, args.retry, args.retry_wait)

    def setup_runner(self, args, enable_options, disable_options, runner):
        self.check_bool_option(args, 'strip', enable_options, disable_options, 'zig-')
        self.check_bool_option(args, 'single-threaded', enable_options, disable_options, 'zig-')
        enable_options.append('zig-mode-{}'.format(args.std_cxx.lower()))

        super(ZigCLI, self).setup_runner(args, list(set(enable_options)), disable_options, runner)


def zig(compiler=None):
    cli = ZigCLI(compiler)
    cli.execute()


def main():
    zig()


if __name__ == '__main__':
    main()
