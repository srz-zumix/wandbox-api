import glob
import re
import os

from .cli import CLI
from .runner import Runner


class CrystalRunner(Runner):

    REQUIRE_REGEX = re.compile(r'^\s*require\s+(.*?)$')

    def reset(self):
        self.required = []

    def make_code(self, file, filepath, filename):
        files = dict()
        code = ''
        for line in file:
            m = self.REQUIRE_REGEX.match(line)
            if m:
                module = m.group(1).strip('\'"')
                files.update(self.require(os.path.dirname(filepath), module.strip()))
            code += line
        files[filename] = code
        return files

    def require_glob(self, path, module_name_):
        files = dict()
        for x in glob.glob(os.path.join(path, module_name_), recursive=True):
            if os.path.isfile(x):
                files.update(self.require_file(path, x))
        return files

    def require_file(self, path, module_name_):
        files = dict()
        module_name = os.path.normpath(module_name_)
        if module_name in self.required:
            return files
        module_file = module_name
        module_path = os.path.normpath(os.path.join(path, module_file))
        if not os.path.exists(module_path):
            module_file = module_name + '.cr'
            module_path = os.path.normpath(os.path.join(path, module_file))
        if os.path.exists(module_path):
            self.required.append(module_name)
            files.update(self.open_code(module_path, module_file))
        return files

    def require(self, path, module_name_):
        if '*' in module_name_:
            return self.require_glob(path, module_name_)
        else:
            return self.require_file(path, module_name_)


class CrystalCLI(CLI):

    def __init__(self, compiler=None):
        super(CrystalCLI, self).__init__('Crystal', compiler, False, False)

    def get_runner(self, args, options):
        return CrystalRunner(args.language, args.compiler, args.save, args.encoding, args.retry, args.retry_wait)


def crystal(compiler=None):
    cli = CrystalCLI(compiler)
    cli.execute()


def main():
    crystal()


if __name__ == '__main__':
    main()
