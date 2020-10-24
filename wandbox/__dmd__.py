from .cli import CLI


class DmdCLI(CLI):

    def __init__(self, compiler=None):
        super(DmdCLI, self).__init__('D', compiler, False)


def dmd(compiler=None):
    cli = DmdCLI(compiler)
    cli.execute()


def main():
    dmd()


if __name__ == '__main__':
    main()
