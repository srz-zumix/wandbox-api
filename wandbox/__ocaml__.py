from .cli import CLI


class OCamlCLI(CLI):

    def __init__(self, compiler=None):
        super(OCamlCLI, self).__init__('OCaml', compiler, False)


def ocaml(compiler=None):
    cli = OCamlCLI(compiler)
    cli.execute()


def main():
    ocaml()


if __name__ == '__main__':
    main()
