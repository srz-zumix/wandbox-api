import re
import os

from .cli import CLI
from .runner import Runner


class JuliaRunner(Runner):

    INCLUDE_REGEX = re.compile(r'^\s*include\s*\((.*?)\)\s*$')

    def reset(self):
        self.included = []

    def make_code(self, file, filepath, filename):
        files = dict()
        code = ''
        for line in file:
            m = self.INCLUDE_REGEX.match(line)
            if m:
                module = m.group(1).strip('(\'")')
                files.update(self.include(os.path.dirname(filepath), module.strip()))
            code += line
        files[filename] = code
        return files

    def include(self, path, module_name_):
        files = dict()
        module_name = os.path.normpath(module_name_)
        if module_name in self.included:
            return files
        module_file = module_name
        module_path = os.path.normpath(os.path.join(path, module_file))
        if os.path.exists(module_path):
            self.included.append(module_name)
            files.update(self.open_code(module_path, module_file))
        return files


class JuliaCLI(CLI):

    def __init__(self, compiler=None):
        super(JuliaCLI, self).__init__('Julia', compiler, False, False)

    def get_runner(self, args, options):
        return JuliaRunner(args.language, args.compiler, args.save, args.encoding, args.retry, args.retry_wait)


def julia(compiler=None):
    cli = JuliaCLI(compiler)
    cli.execute()


def main():
    julia()


if __name__ == '__main__':
    main()
