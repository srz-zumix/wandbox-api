import os
import re

from .cli import CLI
from .runner import Runner


class LuaRunner(Runner):

    REQUIRE_REGEX = re.compile(r'.*require\s*(.*?);.*')
    LOADFILE_REGEX = re.compile(r'.*loadfile\s*(.*?);.*')

    def reset(self):
        self.required = []

    def make_code(self, file, filepath, filename):
        files = dict()
        code = ''
        for line in file:
            m = self.REQUIRE_REGEX.match(line)
            if m:
                module = m.group(1).strip('(\'")')
                files.update(self.require(os.path.dirname(filepath), module.strip()))
            else:
                m = self.LOADFILE_REGEX.match(line)
                if m:
                    module = m.group(1).strip('(\'")')
                    files.update(self.require(os.path.dirname(filepath), module.strip()))
            code += line
        files[filename] = code
        return files

    def require(self, path, module_name_):
        files = dict()
        module_name = os.path.normpath(module_name_)
        if module_name in self.required:
            return files
        module_file = module_name
        module_path = os.path.normpath(os.path.join(path, module_file))
        if not os.path.exists(module_path):
            module_file = module_name + '.lua'
            module_path = os.path.normpath(os.path.join(path, module_file))
        if os.path.exists(module_path):
            self.required.append(module_name)
            files.update(self.open_code(module_path, module_file))
        return files


class LuaCLI(CLI):

    def __init__(self, compiler=None):
        super(LuaCLI, self).__init__('Lua', compiler, False, False)

    def get_runner(self, args, options):
        return LuaRunner(args.language, args.compiler, args.save, args.encoding, args.retry, args.retry_wait)


def lua(compiler=None):
    cli = LuaCLI(compiler)
    cli.execute()


def main():
    lua()


def luajit():
    lua('luajit-*')


if __name__ == '__main__':
    main()
