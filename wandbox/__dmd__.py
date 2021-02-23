from .cli import CLI


class DCLI(CLI):

    def __init__(self, compiler=None):
        super(DCLI, self).__init__('D', compiler, False)


def dmd(compiler=None):
    cli = DCLI(compiler)
    cli.execute()


def main():
    dmd()


def gdmd():
    cli = DCLI('gdc-*')
    cli.execute()


def ldmd2():
    cli = DCLI('ldc-*')
    cli.execute()


if __name__ == '__main__':
    main()
