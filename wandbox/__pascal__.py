import re
import os

from .utils import case_insensitive_glob
from .cli import CLI
from .runner import Runner


class PascalRunner(Runner):

    INCLUDE_REGEX = re.compile(r'^\s*{\$(I|INCLUDE)\s+(.*)}\s*$')
    USES_REGEX = re.compile(r'^\s*uses\s*(.*)')
    USES_IN_REGEX = re.compile(r'^\s*.*\s*in\s*(.*)')

    def reset(self):
        self.included = []

    def make_code(self, file, filepath, filename):
        files = dict()
        code = ''
        uses = None
        for line in file:
            if uses is not None:
                uses += line
                if ';' in uses:
                    files.update(self.parse_uses(os.path.dirname(filepath), uses))
                    uses = None
            m = self.INCLUDE_REGEX.match(line)
            if m:
                module = m.group(2).strip('\'"')
                files.update(self.include(os.path.dirname(filepath), module.strip()))
            else:
                m = self.USES_REGEX.match(line)
                if m:
                    uses = m.group(1)
            code += line
        files[filename] = code
        return files

    def parse_uses(self, filepath, uses):
        files = dict()
        for token in uses.split(','):
            module_name = token.strip().strip(';')
            m = self.USES_IN_REGEX.match(module_name)
            if m:
                module_name = m.group(1).strip('\'"')
            if module_name:
                files.update(self.include(filepath, module_name))
        return files

    def find_file(self, path, module_name):
        module_path = os.path.normpath(os.path.join(path, module_name))
        if os.path.exists(module_path):
            return module_path, module_name
        for ext in ['.pas', '.pp', '.inc']:
            module_file = module_name + ext
            m = case_insensitive_glob(path, module_file)
            if len(m) == 1:
                return m[0], os.path.basename(m[0])
        return None, None

    def include(self, path, module_name_):
        files = dict()
        module_name = os.path.normpath(module_name_)
        if module_name in self.included:
            return files
        module_path, module_file = self.find_file(path, module_name)
        if module_path:
            self.included.append(module_name)
            files.update(self.open_code(module_path, module_file))
        return files


class PascalCLI(CLI):

    def __init__(self, compiler=None):
        super(PascalCLI, self).__init__('Pascal', compiler)
        self.pacal_setup('Pascal', compiler)

    def pacal_setup(self, lang, compiler):
        self.parser.add_argument(
            '--delphi-mode',
            action='store_true',
            help='set -Mdelphi'
        )

    def setup_runner(self, args, enable_options, disable_options, runner):
        self.check_bool_option(args, 'delphi-mode', enable_options, disable_options)

        super(PascalCLI, self).setup_runner(args, list(set(enable_options)), disable_options, runner)

    def get_runner(self, args, options):
        return PascalRunner(args.language, args.compiler, args.save, args.encoding, args.retry, args.retry_wait)


def pascal(compiler=None):
    cli = PascalCLI(compiler)
    cli.execute()


def main():
    pascal()


if __name__ == '__main__':
    main()
