import re
import os

from .cli import CLI
from .runner import Runner


class JsRunner(Runner):

    IMPORT_REGEX = re.compile(r'^\s*import\s+.*?\s+from\s+(.*?)[;|]$')
    REQUIRE_REGEX = re.compile(r'^\s.*?require\s+\((.*?)\)')

    def __init__(self, lang, compiler, save, encoding, retry, retry_wait, prefix_chars='-'):
        self.configs = ['package.json']
        super(JsRunner, self).__init__(lang, compiler, save, encoding, retry, retry_wait, prefix_chars)

    def reset(self):
        self.imported = []

    def make_code(self, file, filepath, filename):
        files = dict()
        code = ''
        for config in self.configs:
            config_path_name = os.path.join(os.path.dirname(filename), config)
            config_path = os.path.join(os.path.dirname(filepath), config)
            if os.path.exists(config_path):
                files.update(self.import_from(os.path.dirname(config_path), config_path_name))
        for line in file:
            m = self.IMPORT_REGEX.match(line)
            if m:
                module = m.group(1).strip('\'"')
                if module.startswith('.'):
                    files.update(self.import_from(os.path.dirname(filepath), module.strip()))
            code += line
        files[filename] = code
        return files

    def import_from(self, path, module_name_):
        files = dict()
        module_name = os.path.normpath(module_name_)
        if module_name in self.imported:
            return files
        module_path = os.path.normpath(os.path.join(path, module_name))
        if not os.path.exists(module_path):
            return files
        if os.path.isdir(module_path):
            for f in os.listdir(module_path):
                package_path = os.path.join(module_name, f)
                path = os.path.join(module_path, f)
                files.update(self.import_from(path, package_path))
        elif os.path.isfile(module_path):
            self.imported.append(module_name)
            files.update(self.open_code(module_path, module_name))
        return files


class JsCLI(CLI):

    def __init__(self, compiler=None):
        super(JsCLI, self).__init__('JavaScript', compiler, False, False)

    def get_runner(self, args, options):
        return JsRunner(args.language, args.compiler, args.save, args.encoding, args.retry, args.retry_wait)


def js(compiler=None):
    cli = JsCLI(compiler)
    cli.execute()


def main():
    js()


def node():
    js('nodejs-*')


def spidermonkey():
    js('spidermonkey-*')


if __name__ == '__main__':
    main()
