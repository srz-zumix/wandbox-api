import re
import os

from .cli import CLI
from .runner import Runner


class RubyRunner(Runner):

    REQUIRE_REGEX = re.compile(r'^\s*require\s+(.*?)$')
    REQUIRE_RELATIVE_REGEX = re.compile(r'^\s*require_relative\s+(.*?)$')

    def reset(self):
        self.required = []

    def make_code(self, file, filepath, filename):
        files = dict()
        code = ''
        for line in file:
            m = self.REQUIRE_REGEX.match(line)
            if m:
                module = m.group(1).strip('\'"')
                if module.startswith('.'):
                    files.update(self.require(os.path.dirname(filepath), module.strip()))
            else:
                m = self.REQUIRE_RELATIVE_REGEX.match(line)
                if m:
                    module = m.group(1).strip('\'"')
                    files.update(self.require(os.path.dirname(filepath), module.strip()))
            code += line
        files[filename] = code
        return files

    def require(self, path, module_name_):
        files = dict()
        module_name = os.path.normpath(module_name_)
        if module_name in self.required:
            return files
        module_file = module_name + '.rb'
        module_path = os.path.normpath(os.path.join(path, module_file))
        if os.path.exists(module_path):
            self.required.append(module_name)
            files.update(self.open_code(module_path, module_file))
        return files


class RubyCLI(CLI):

    def __init__(self, compiler=None):
        super(RubyCLI, self).__init__('Ruby', compiler, False, False)

    def get_runner(self, args, options):
        return RubyRunner(args.language, args.compiler, args.save, args.encoding, args.retry, args.retry_wait)


def ruby(compiler=None):
    cli = RubyCLI(compiler)
    cli.execute()


def main():
    ruby()


def mruby():
    ruby('mruby-*')


if __name__ == '__main__':
    main()
