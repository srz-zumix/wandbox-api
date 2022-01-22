from .cli import CLI
from .runner import Runner


class SqlRunner(Runner):

    def build_compiler_options(self, options):
        try:
            super(SqlRunner, self).build_compiler_options(options)
        except Exception:
            options.append('-')
            super(SqlRunner, self).build_compiler_options(options)


class SqlCLI(CLI):

    def __init__(self, compiler=None):
        super(SqlCLI, self).__init__('SQL', compiler, False, False, run_source_nargs='*')

    def get_runner(self, args, options):
        return SqlRunner(args.language, args.compiler, args.save, args.encoding, args.retry, args.retry_wait)


def sql(compiler=None):
    cli = SqlCLI(compiler)
    cli.execute()


def main():
    sql()


if __name__ == '__main__':
    main()
