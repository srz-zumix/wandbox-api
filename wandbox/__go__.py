import os
import re

from .runner import Runner
from .cli import CLI


class GoRunner(Runner):

    IMPORT_REGEX = re.compile(r'^\s*import\s+(.*?)$')
    IMPORT_MULTILINE_REGEX = re.compile(r'import\s+\((.*?)\)', re.MULTILINE | re.DOTALL)

    def reset(self):
        self.imported = []
        self.incdirs = []

    def make_code(self, file, filepath, filename):
        files = dict()
        code = ''
        for line in file:
            m = self.IMPORT_REGEX.match(line)
            if m:
                files.update(self.on_import_single(filepath, m.group(1).strip('(\'")')))
            code += line
        for m in self.IMPORT_MULTILINE_REGEX.finditer(code):
            files.update(self.on_import_multiline(filepath, m.group(1)))
        files[filename] = code
        return files

    def on_import_multiline(self, filepath, imports):
        files = dict()
        for line in imports.splitlines():
            names = line.split()
            if len(names) == 1:
                files.update(self.on_import_single(filepath, names[0].strip('(\'")')))
            elif len(names) > 1:
                files.update(self.on_import_single(filepath, names[1].strip('(\'")')))
        return files

    def on_import_single(self, filepath, filename):
        files = dict()
        if filename.startswith('.'):
            path = os.path.join(os.path.dirname(filepath), filename)
            if os.path.isdir(path):
                path = os.path.normpath(path)
                if path not in self.imported:
                    self.imported.append(path)
                    files.update(self.on_import(path, filename))
        return files

    def on_import(self, filepath, packagepath):
        files = dict()
        for f in os.listdir(filepath):
            go_filepath = os.path.join(filepath, f)
            if os.path.isfile(go_filepath) and f.endswith('.go'):
                files.update(self.open_code(go_filepath, go_filepath))
        return files


class GoCLI(CLI):

    def __init__(self, compiler=None):
        super(GoCLI, self).__init__('Go', compiler)
        self.go_setup('Go', compiler)

    def go_setup(self, lang, compiler):
        self.parser.add_argument(
            '--gcflags-m',
            action='store_true',
            help='set -gcflags -m'
        )

    def get_runner(self, args, options):
        return GoRunner(args.language, args.compiler, args.save, args.encoding, args.retry, args.retry_wait)

    def setup_runner(self, args, enable_options, disable_options, runner):
        self.check_bool_option(args, 'gcflags-m', enable_options, disable_options, 'go-')
        runner.has_runtime_option_raw = False

        super(GoCLI, self).setup_runner(args, list(set(enable_options)), disable_options, runner)


def golang(compiler=None):
    cli = GoCLI(compiler)
    cli.execute()


def main():
    golang()


if __name__ == '__main__':
    main()
