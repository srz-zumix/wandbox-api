from .cli import CLI


class GoCLI(CLI):

    def __init__(self, compiler=None):
        super(GoCLI, self).__init__('Go', compiler)
        self.go_setup('Go', compiler)

    def go_setup(self, lang, compiler):
        self.parser.add_argument(
            '--gcflags-m',
            action='store_true',
            help='set -gcflags -m'
        )

    def setup_runner(self, args, enable_options, disable_options, runner):
        self.check_bool_option(args, 'gcflags-m', enable_options, disable_options, 'go-')
        runner.has_runtime_option_raw = False

        super(GoCLI, self).setup_runner(args, list(set(enable_options)), disable_options, runner)


def golang(compiler=None):
    cli = GoCLI(compiler)
    cli.execute()


def main():
    golang()


if __name__ == '__main__':
    main()
