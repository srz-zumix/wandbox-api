from .cli import CLI


class VimCLI(CLI):

    def __init__(self, compiler=None):
        super(VimCLI, self).__init__('Vim script', compiler, False, False, run_prefix_chars='@')


def vim(compiler=None):
    cli = VimCLI(compiler)
    cli.execute()


def main():
    vim()


if __name__ == '__main__':
    main()
