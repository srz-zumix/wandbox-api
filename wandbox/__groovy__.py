import re
import os
import glob

from .cli import CLI
from .runner import Runner


class GroovyRunner(Runner):

    IMPORT_REGEX = re.compile(r'^\s*import\s+(.*?)$')

    def reset(self):
        self.imported = []

    def open_main_code(self, filepath, filename):
        files = super(GroovyRunner, self).open_main_code(filepath, filename)
        if filepath != '-':
            files.update(self.import_module(os.path.dirname(filepath), '*'))
        return files

    def make_code(self, file, filepath, filename):
        files = dict()
        code = ''
        for line in file:
            m = self.IMPORT_REGEX.match(line)
            if m:
                module = m.group(1).strip('\'";')
                files.update(self.import_module(os.path.dirname(filepath), module.strip()))
            code += line
        files[filename] = code
        return files

    def module_path_to_glob(self, path, module_name):
        s = module_name.replace(".", "/")
        return os.path.join(path, s + ".groovy")

    def import_module(self, path, module_name_):
        files = dict()
        for x in glob.glob(self.module_path_to_glob(path, module_name_)):
            if os.path.isfile(x):
                if x not in self.imported:
                    self.imported.append(x)
                    files.update(self.open_code(os.path.join(path, x), x))
        return files


class GroovyCLI(CLI):

    def __init__(self, compiler=None):
        super(GroovyCLI, self).__init__('Groovy', compiler, False, False)

    def get_runner(self, args, options):
        return GroovyRunner(args.language, args.compiler, args.save, args.encoding, args.retry, args.retry_wait)


def groovy(compiler=None):
    cli = GroovyCLI(compiler)
    cli.execute()


def main():
    groovy()


if __name__ == '__main__':
    main()
