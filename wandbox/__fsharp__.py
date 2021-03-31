from .cli import CLI


class FsCLI(CLI):

    def __init__(self, compiler=None):
        super(FsCLI, self).__init__('F#', compiler, False)


def fsharp(compiler=None):
    cli = FsCLI(compiler)
    cli.execute()


def main():
    fsharp()


if __name__ == '__main__':
    main()
