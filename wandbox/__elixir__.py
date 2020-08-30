import re
import os

from .cli import CLI


class ElixirCLI(CLI):

    def __init__(self, compiler=None):
        super(ElixirCLI, self).__init__('Elixir', compiler, False, False)


def elixir(compiler=None):
    cli = ElixirCLI(compiler)
    cli.execute()


def main():
    elixir()


if __name__ == '__main__':
    main()
