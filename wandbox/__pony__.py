import sys
import os
import glob

from .cli import CLI
from .runner import Runner

dummy_src_option = '@@dummy_src_option'


class PonyRunner(Runner):

    def replace_path(self, path, new_dir):
        if new_dir:
            return os.path.join(new_dir, os.path.basename(path))
        else:
            return path

    def resolve_build_dir(self, build_dirs, dir):
        if dir in build_dirs:
            index = 0
            while True:
                dir = 'prog{0}'.format(index)
                if dir not in build_dirs:
                    break
                index += 1
        return dir

    def build_compiler_options(self, options):
        paths = []
        reserved_build_dirs = ['prog', '.']
        build_dirs = []
        for opt in options:
            if opt == dummy_src_option:
                continue
            if opt[0] in self.prefix_chars:
                self.add_commandline_options(opt)
            else:
                if os.path.isfile(opt):
                    raise Exception('Error: {0}: couldn\'t locate this path'.format(opt))
                elif os.path.isdir(opt):
                    dir = self.resolve_build_dir(reserved_build_dirs, opt)
                    reserved_build_dirs.append(dir)
                    paths.append({'wandbox': dir, 'path': opt})
                    build_dirs.append(dir)
                else:
                    self.add_commandline_options(opt)
        if len(paths) == 0:
            dir = self.resolve_build_dir(reserved_build_dirs, '.')
            reserved_build_dirs.append(dir)
            paths.append({'wandbox': dir, 'path': '.'})
            build_dirs.append(dir)
        codes = {}
        for pair in paths:
            path = pair['path']
            wandbox_dir = pair['wandbox']
            for x in glob.glob(os.path.join(path, '*.pony')):
                files = self.open_code(x, x)
                for k, v in files.items():
                    codes[self.replace_path(k, wandbox_dir)] = v

        dummy_code = """
actor Main
  new create(env: Env) =>
    env.out.print("Dummy main")
        """
        if len(codes) == 1:
            self.wandbox.code(list(codes.values())[0])
        else:
            self.wandbox.code(dummy_code)
            for k, v in codes.items():
                self.wandbox.add_file(k, v)
            for dir in build_dirs:
                self.add_commandline_options(dir)
            self.add_compiler_options('-b=prog')


class PonyCLI(CLI):

    def __init__(self, compiler=None):
        super(PonyCLI, self).__init__('Pony', compiler, False)

    def get_runner(self, args, options):
        return PonyRunner(args.language, args.compiler, args.save, args.encoding, args.retry, args.retry_wait)

    def execute(self):
        args = sys.argv[1:]
        if '.' not in args:
            args.append(dummy_src_option)
        self.execute_with_args(args)


def pony(compiler=None):
    cli = PonyCLI(compiler)
    cli.execute()


def main():
    pony()


if __name__ == '__main__':
    main()
