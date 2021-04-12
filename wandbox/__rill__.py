from .cli import CLI


class RillCLI(CLI):

    def __init__(self, compiler=None):
        super(RillCLI, self).__init__('Rill', compiler, False)


def rill(compiler=None):
    cli = RillCLI(compiler)
    cli.execute()


def main():
    rill()


if __name__ == '__main__':
    main()
