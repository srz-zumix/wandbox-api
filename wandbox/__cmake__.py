import re
import os

from .cli import CLI
from .runner import Runner


class CMakeRunner(Runner):

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


class CMakeCLI(CLI):

    def __init__(self, compiler=None):
        super(CMakeCLI, self).__init__('CMake', compiler, False, False)

    def get_runner(self, args, options):
        return CMakeRunner(args.language, args.compiler, args.save, args.encoding, args.retry, args.retry_wait)


def cmake(compiler=None):
    cli = CMakeCLI(compiler)
    cli.execute()


def main():
    cmake()


if __name__ == '__main__':
    main()
