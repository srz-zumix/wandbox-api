import re
import os
import ast

from .cli import CLI
from .runner import Runner


def _show(node):
    for name, val in ast.iter_fields(node):
        print("{name}: {val}".format(name=name, val=val))


class SetUpVisitor(ast.NodeVisitor):

    def __init__(self):
        self.packages = []

    def append_testsuite(self, testsuite):
        path = testsuite.split('.')
        self.packages.append(path[0])

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id == "setup":
                for keyword in node.keywords:
                    if keyword.arg == "packages":
                        if isinstance(keyword.value, ast.List):
                            for package in keyword.value.elts:
                                self.packages.append(package.value)
                        elif isinstance(keyword.value, ast.Str):
                            self.packages.append(keyword.value.value)
                    if keyword.arg == "test_suite":
                        if isinstance(keyword.value, ast.List):
                            for package in keyword.value.elts:
                                self.append_testsuite(package.value)
                        elif isinstance(keyword.value, ast.Str):
                            self.append_testsuite(keyword.value.value)


class PythonRunner(Runner):

    IMPORT_REGEX = re.compile(r'^\s*import\s*(.*?)(\s*as\s*\S*|)$')
    FROM_IMPORT_REGEX = re.compile(r'^\s*from\s*(\S*?)\s*import\s*(.*?)(\s*as\s*\S*|)$')

    def reset(self):
        self.imports = []

    def get_imports(self, path, module_name):
        if path == module_name:
            return self.make_from_package(path, module_name)
        module_file = module_name + '.py'
        module_path = os.path.normpath(os.path.join(path, module_file))
        if os.path.exists(module_path):
            module_abspath = os.path.abspath(module_path)
            if module_abspath not in self.imports:
                self.imports.append(module_abspath)
                return self.open_code(module_path, module_file)
        return dict()

    def make_code(self, file, filepath, filename):
        if os.path.basename(filepath) == 'setup.py':
            return self.make_from_setup_py(filepath, filename)
        files = dict()
        code = ''
        for line in file:
            m = self.IMPORT_REGEX.match(line)
            if m:
                modules = m.group(1)
                for module_name in modules.split(','):
                    files.update(self.get_imports(os.path.dirname(filepath), module_name.strip()))
            else:
                m = self.FROM_IMPORT_REGEX.match(line)
                if m:
                    module = m.group(1)
                    module_names = module.split('.')
                    if len(module_names) == 0:
                        files.update(self.get_imports(os.path.dirname(filepath), os.path.dirname(filepath)))
                    else:
                        module_name = os.path.join(*module_names)
                        if module.startswith('.'):
                            name = os.path.join(os.path.dirname(filename), module_name)
                            files.update(self.get_imports(os.path.dirname(filepath), name))
                        else:
                            files.update(self.get_imports(os.path.dirname(filepath), module_name))
            code += line
        files[filename] = code
        # print(files.keys())
        return files

    def make_from_setup_py(self, filepath, filename):
        files = dict()
        code = ''
        file = self.file_open(filepath, 'r')
        code = file.read()
        tree = ast.parse(code)
        setup = SetUpVisitor()
        setup.visit(tree)
        root = os.path.dirname(filepath)
        for package in setup.packages:
            module_path = os.path.join(root, package)
            files.update(self.make_from_package(module_path, package))
        files[filename] = code
        return files

    def make_from_package(self, dirpath, dirname_):
        files = dict()
        dirname = os.path.normpath(dirname_)
        if dirpath in self.imports:
            return files
        if os.path.exists(dirpath):
            self.imports.append(dirpath)
            for f in os.listdir(dirpath):
                package_path = os.path.join(dirname, f)
                path = os.path.join(dirpath, f)
                if os.path.isdir(path):
                    package_codes = self.make_from_package(path, package_path)
                    files.update(package_codes)
                elif os.path.isfile(path):
                    name, ext = os.path.splitext(path)
                    if ext == '.pyc':
                        continue
                    package_codes = self.open_code(path, package_path)
                    files.update(package_codes)
        return files


class PythonCLI(CLI):

    def __init__(self, compiler=None):
        super(PythonCLI, self).__init__('Python', compiler, False, False)

    def get_runner(self, args, options):
        return PythonRunner(args.language, args.compiler, args.save, args.encoding, args.retry, args.retry_wait)


def python(compiler=None):
    cli = PythonCLI(compiler)
    cli.execute()


def main():
    python()


def python2():
    python('cpython-2.7-*')


def python3():
    python('cpython-*')


def pypy():
    python('pypy-*')


if __name__ == '__main__':
    main()
