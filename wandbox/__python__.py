import re
import os

from .cli import CLI
from .runner import Runner


class PythonRunner(Runner):

    IMPORT_REGEX = re.compile(r'^\s*import\s*(.*?)(\s*as\s*\S*|)$')
    FROM_IMPORT_REGEX = re.compile(r'^\s*from\s*(\S*?)\s*import\s*(.*?)(\s*as\s*\S*|)$')
    imports = []

    def get_imports(self, path, module_name):
        module_path = os.path.normpath(os.path.join(path, module_name + '.py'))
        if os.path.exists(module_path):
            module_abspath = os.path.abspath(module_path)
            if module_abspath not in self.imports:
                self.imports.append(module_abspath)
                return self.open_code(module_path, module_path)
        return []

    def make_code(self, filepath, filename):
        files = dict()
        code = ''
        file = self.file_open(filepath, 'r')
        for line in file:
            m = self.IMPORT_REGEX.match(line)
            if m:
                modules = m.group(1)
                for module_name in modules.split(','):
                    files.update(self.get_imports(os.path.dirname(filepath), module_name.strip()))
            else:
                m = self.FROM_IMPORT_REGEX.match(line)
                if m:
                    module = m.group(1)
                    module_names = module.split('.')
                    module_name = os.path.join(*module_names)
                    files.update(self.get_imports(os.path.dirname(filepath), module_name))
            code += line
        file.close()
        files[filename] = code
        return files


class PythonCLI(CLI):

    def __init__(self, compiler=None):
        super(PythonCLI, self).__init__('Python', compiler)

    def get_runner(self, args, options):
        return PythonRunner(args.language, args.compiler, args.save, args.encoding, args.retry, args.retry_wait, False)


def python(compiler=None):
    cli = PythonCLI(compiler)
    cli.execute()


def main():
    python()


def python2():
    python('cpython-2.7-head')


def python3():
    python('cpython-head')


def pypy():
    python('pypy-head')


if __name__ == '__main__':
    main()
