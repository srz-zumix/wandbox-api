from .cli import CLI


class ErlangCLI(CLI):

    def __init__(self, compiler=None):
        super(ErlangCLI, self).__init__('Erlang', compiler, False)


def erlang(compiler=None):
    cli = ErlangCLI(compiler)
    cli.execute()


def main():
    erlang()


if __name__ == '__main__':
    main()
