from .cli import CLI


class CsCLI(CLI):

    def __init__(self, compiler=None):
        super(CsCLI, self).__init__('C#', compiler)
        self.cs_setup('C#', compiler)

    def cs_setup(self, lang, compiler):
        self.parser.add_argument(
            '--optimize',
            action='store_true',
            help='use optimization'
        )

    def setup_runner(self, args, enable_options, disable_options, runner):
        self.check_bool_option(args, 'optimize'     , enable_options, disable_options)
        super(CsCLI, self).setup_runner(args, list(set(enable_options)), disable_options, runner)


def csharp(compiler=None):
    cli = CsCLI(compiler)
    cli.execute()


def main():
    csharp()


if __name__ == '__main__':
    main()
