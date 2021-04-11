import glob

from .cli import CLI
from .runner import Runner


class ScalaRunner(Runner):

    def open_code(self, filepath, filename):
        files = dict()
        for x in glob.glob(filepath):
            files.update(super(ScalaRunner, self).open_code(x, x))
        return files


class ScalaCLI(CLI):

    def __init__(self, compiler=None):
        super(ScalaCLI, self).__init__('Scala', compiler, False)

    def get_runner(self, args, options):
        return ScalaRunner(args.language, args.compiler, args.save, args.encoding, args.retry, args.retry_wait)


def scala(compiler=None):
    cli = ScalaCLI(compiler)
    cli.execute()


def main():
    scala()


if __name__ == '__main__':
    main()
