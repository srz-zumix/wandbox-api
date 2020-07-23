import re
import os

from .cli import CLI

class PythonCLI(CLI):

    def __init__(self, compiler=None):
        super(PythonCLI, self).__init__('Python', compiler)


def python(compiler=None):
    cli = PythonCLI(compiler)
    cli.execute()


def main():
    python()


def python2():
    python('cpython-2.7-head')


def python3():
    python('cpython-head')


def pypy():
    python('pypy-head')


if __name__ == '__main__':
    main()
