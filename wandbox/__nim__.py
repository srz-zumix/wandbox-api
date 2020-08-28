import re
import os

from .cli import CLI
from .runner import Runner


class NimRunner(Runner):

    IMPORT_REGEX = re.compile(r'^\s*import\s*(.*?)(\s*except\s*.*|)$')
    FROM_IMPORT_REGEX = re.compile(r'^\s*from\s*(\S*?)\s*import\s*(.*?)$')

    def reset(self):
        self.imports = []

    def make_code(self, file, filepath, filename):
        files = dict()
        code = ''
        for line in file:
            m = self.IMPORT_REGEX.match(line)
            if m:
                modules = m.group(1).strip('\'"')
                for module_name in modules.split(','):
                    files.update(self.get_imports(os.path.dirname(filepath), module_name.strip()))
            else:
                m = self.FROM_IMPORT_REGEX.match(line)
                if m:
                    module = m.group(1).strip('\'"')
                    module_names = module.split('.')
                    if len(module_names) == 0:
                        files.update(self.get_imports(os.path.dirname(filepath), os.path.dirname(filepath)))
                    else:
                        module_name = os.path.join(*module_names)
                        files.update(self.get_imports(os.path.dirname(filepath), module_name))
            code += line
        files[filename] = code
        return files

    def get_imports(self, path, module_name):
        module_file = module_name + '.nim'
        module_path = os.path.normpath(os.path.join(path, module_file))
        if os.path.exists(module_path):
            module_abspath = os.path.abspath(module_path)
            if module_abspath not in self.imports:
                self.imports.append(module_abspath)
                return self.open_code(module_path, module_file)
        return dict()


class NimCLI(CLI):

    def __init__(self, compiler=None):
        super(NimCLI, self).__init__('Nim', compiler, False)

    def get_runner(self, args, options):
        return NimRunner(args.language, args.compiler, args.save, args.encoding, args.retry, args.retry_wait)


def nim(compiler=None):
    cli = NimCLI(compiler)
    cli.execute()


def main():
    nim()


if __name__ == '__main__':
    main()
