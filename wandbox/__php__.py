import re
import os

from .cli import CLI
from .runner import Runner


class PhpRunner(Runner):

    REQUIRE_INCLUDE_REGEX = re.compile(r'.*(require|require_once|include|include_once)\s*[\'"\(\)](.*?)[\'"\(\)]\s*;$')

    def reset(self):
        self.required = []
        self.incdirs = []

    def make_code(self, file, filepath, filename):
        files = dict()
        code = ''
        for line in file:
            m = self.REQUIRE_INCLUDE_REGEX.match(line)
            if m:
                path = m.group(2).strip('\'"()')
                files.update(self.require(os.path.dirname(filepath), path.strip()))
            code += line
        files[filename] = code
        return files

    def require_resolve_path(self, path, file_name):
        if os.path.exists(file_name):
            return file_name
        file_path = os.path.join(path, file_name)
        if os.path.exists(file_path):
            return file_name
        for ipath in self.incdirs:
            file_path = os.path.join(path, file_name)
            if os.path.exists(file_path):
                return file_name
        return None


    def require(self, path, file_name_):
        files = dict()
        file_name = os.path.normpath(file_name_)
        file_path = self.require_resolve_path(path, file_name)
        if file_path:
            if file_path not in self.required:
                self.required.append(file_path)
                files.update(self.open_code(file_path, file_name))
        return files


class PhpCLI(CLI):

    def __init__(self, compiler=None):
        super(PhpCLI, self).__init__('PHP', compiler, False, False)

    def get_runner(self, args, options):
        return PhpRunner(args.language, args.compiler, args.save, args.encoding, args.retry, args.retry_wait)


def php(compiler=None):
    cli = PhpCLI(compiler)
    cli.execute()


def main():
    php()


if __name__ == '__main__':
    main()
