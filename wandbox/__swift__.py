from .cli import CLI


class SwiftCLI(CLI):

    def __init__(self, compiler=None):
        super(SwiftCLI, self).__init__('Swift', compiler, False)


def swift(compiler=None):
    cli = SwiftCLI(compiler)
    cli.execute()


def main():
    swift()


if __name__ == '__main__':
    main()
