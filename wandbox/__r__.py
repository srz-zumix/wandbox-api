import re
import os

from .cli import CLI
from .runner import Runner


class RscriptRunner(Runner):

    SOURCE_REGEX = re.compile(r'^\s*source\s*\((.*?)\)\s*$')

    def reset(self):
        self.sourced = []

    def make_code(self, file, filepath, filename):
        files = dict()
        code = ''
        for line in file:
            m = self.SOURCE_REGEX.match(line)
            if m:
                module = m.group(1).strip('(\'")')
                files.update(self.source(os.path.dirname(filepath), module.strip()))
            code += line
        files[filename] = code
        return files

    def source(self, path, module_name_):
        files = dict()
        module_name = os.path.normpath(module_name_)
        if module_name in self.sourced:
            return files
        module_file = module_name
        module_path = os.path.normpath(os.path.join(path, module_file))
        if os.path.exists(module_path):
            self.sourced.append(module_name)
            files.update(self.open_code(module_path, module_file))
        return files


class RscriptCLI(CLI):

    def __init__(self, compiler=None):
        super(RscriptCLI, self).__init__('R', compiler, False, False)

    def get_runner(self, args, options):
        return RscriptRunner(args.language, args.compiler, args.save, args.encoding, args.retry, args.retry_wait)


def rscript(compiler=None):
    cli = RscriptCLI(compiler)
    cli.execute()


def main():
    rscript()


if __name__ == '__main__':
    main()
