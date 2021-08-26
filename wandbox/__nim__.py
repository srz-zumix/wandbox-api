import re
import os

from .cli import CLI
from .runner import Runner
from .__cxx__ import CxxRunner


class NimRunner(Runner):

    IMPORT_REGEX = re.compile(r'^\s*import\s*(.*?)(\s*except\s*.*|)$')
    FROM_IMPORT_REGEX = re.compile(r'^\s*from\s*(\S*?)\s*import\s*(.*?)$')
    C_PROC_REGEX = re.compile(r'^\s*proc.*{.*\.header\s*:\s*([\'"].*[\'"]).*}\s*$')
    PUSH_HEADER_REGEX = re.compile(r'^\s*{\.push\s*.*header\s*:\s*([\'"].*[\'"]).*}$')

    def __init__(self, lang, compiler, save, encoding, retry, retry_wait, prefix_chars='-'):
        super(NimRunner, self).__init__(lang, compiler, save, encoding, retry, retry_wait, prefix_chars)
        self.cxx = CxxRunner(lang, compiler, save, encoding, retry, retry_wait, prefix_chars)

    def reset(self):
        self.imports = []
        self.cxx.reset()

    def make_code(self, file, filepath, filename):
        files = dict()
        code = ''
        for line in file:
            codeline = re.sub(r'\s*#.*$', '', line)
            m = self.IMPORT_REGEX.match(codeline)
            if m:
                files.update(self.get_imports(m, filepath))
            else:
                m = self.FROM_IMPORT_REGEX.match(codeline)
                if m:
                    files.update(self.get_from_imports(m, filepath))
                else:
                    m = self.C_PROC_REGEX.match(codeline)
                    if m:
                        files.update(self.get_c_header(m, filepath))
                    else:
                        m = self.PUSH_HEADER_REGEX.match(codeline)
                        if m:
                            files.update(self.get_c_header(m, filepath))
            code += line
        files[filename] = code
        return files

    def get_c_header(self, m, filepath):
        header = m.group(1).strip('\'"')
        return self.get_c(os.path.dirname(filepath), header)

    def get_c(self, path, filename):
        module_path = os.path.normpath(os.path.join(path, filename))
        if os.path.exists(module_path):
            module_abspath = os.path.abspath(module_path)
            if module_abspath not in self.imports:
                return self.cxx.open_code(module_path, filename)
        return dict()

    def get_from_imports(self, m, filepath):
        files = dict()
        module = m.group(1).strip('\'"')
        module_names = module.split('.')
        if len(module_names) == 0:
            files.update(self.get_import(os.path.dirname(filepath), os.path.dirname(filepath)))
        else:
            module_name = os.path.join(*module_names)
            files.update(self.get_import(os.path.dirname(filepath), module_name))
        return files

    def get_imports(self, m, filepath):
        files = dict()
        modules = m.group(1).strip('\'"')
        for module_name in modules.split(','):
            files.update(self.get_import(os.path.dirname(filepath), module_name.strip()))
        return files

    def get_import(self, path, module_name):
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
