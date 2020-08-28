import re
import os

from .cli import CLI
from .runner import Runner


class PerlRunner(Runner):

    REQUIRE_REGEX = re.compile(r'^\s*require\s+(.*?);$')
    USE_LIB_REGEX = re.compile(r'^\s*use\s+lib\s+(.*?);$')
    UNSHIFT_INC_REGEX = re.compile(r'^\s*unshift\s+@INC\s*,\s*(.*?);$')

    def reset(self):
        self.required = []
        self.incdirs = []

    def make_code(self, file, filepath, filename):
        files = dict()
        code = ''
        for line in file:
            m = self.USE_LIB_REGEX.match(line)
            if m:
                self.add_incdir(filepath, m.group(1))
            m = self.UNSHIFT_INC_REGEX.match(line)
            if m:
                self.add_incdir(filepath, m.group(1))
            m = self.REQUIRE_REGEX.match(line)
            if m:
                module = m.group(1).strip('\'"')
                files.update(self.require(os.path.dirname(filepath), module.strip()))
            code += line
        files[filename] = code
        return files

    def add_incdir(self, filepath, path):
        filedir = os.path.dirname(filepath)
        if len(filedir) == 0:
            filedir = '.'
        path = path.strip('\'"')
        path = path.replace('$FindBin::Bin', filedir)
        self.incdirs.append(path)

    def require(self, path, module_name_):
        files = dict()
        module_name = os.path.normpath(module_name_)
        for ipath in self.incdirs:
            module_file = module_name
            module_path = os.path.normpath(os.path.join(ipath, module_file))
            if not os.path.exists(module_path):
                module_file = module_name + '.pm'
                module_path = os.path.normpath(os.path.join(ipath, module_file))
                if not os.path.exists(module_path):
                    continue
            if module_file in self.required:
                return files
            self.required.append(module_file)
            files.update(self.open_code(module_path, module_file))
        return files


class PerlCLI(CLI):

    def __init__(self, compiler=None):
        super(PerlCLI, self).__init__('Perl', compiler, False, False)

    def get_runner(self, args, options):
        return PerlRunner(args.language, args.compiler, args.save, args.encoding, args.retry, args.retry_wait)


def perl(compiler=None):
    cli = PerlCLI(compiler)
    cli.execute()


def main():
    perl()


if __name__ == '__main__':
    main()
