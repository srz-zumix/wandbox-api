from .cli import CLI


class LazyKCLI(CLI):

    def __init__(self, compiler=None):
        super(LazyKCLI, self).__init__('Lazy K', compiler, False, False)


def lazyk(compiler=None):
    cli = LazyKCLI(compiler)
    cli.execute()


def main():
    lazyk()


if __name__ == '__main__':
    main()
