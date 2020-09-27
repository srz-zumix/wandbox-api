from .cli import CLI


class JavaCLI(CLI):

    def __init__(self, compiler=None):
        super(JavaCLI, self).__init__('Java', compiler, False)


def java(compiler=None):
    cli = JavaCLI(compiler)
    cli.execute()


def main():
    java()


if __name__ == '__main__':
    main()
