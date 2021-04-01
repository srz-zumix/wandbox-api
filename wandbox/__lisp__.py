from .cli import CLI


class LispCLI(CLI):

    def __init__(self, compiler=None):
        super(LispCLI, self).__init__('Lisp', compiler, False, False)


def lisp(compiler=None):
    cli = LispCLI(compiler)
    cli.execute()


def main():
    lisp()


def clisp():
    lisp('clisp-*')


if __name__ == '__main__':
    main()
