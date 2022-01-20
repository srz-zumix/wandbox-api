from .cli import CLI


class OCamlCLI(CLI):

    def __init__(self, compiler=None):
        super(OCamlCLI, self).__init__('OCaml', compiler)
        self.ocaml_setup('OCaml', compiler)

    def ocaml_setup(self, lang, compiler):
        self.parser.add_argument(
            '--no-ocaml-core',
            action='store_true',
            help='disable -package core'
        )

    def command_run_template(self, args):
        # Workaround: ocamlfind: Package `core' not found
        args.no_ocaml_core = True
        super(OCamlCLI, self).command_run_template(args)

    def setup_runner(self, args, enable_options, disable_options, runner):
        self.check_bool_option(args, 'no-ocaml-core', enable_options, disable_options)

        super(OCamlCLI, self).setup_runner(args, list(set(enable_options)), disable_options, runner)


def ocaml(compiler=None):
    cli = OCamlCLI(compiler)
    cli.execute()


def main():
    ocaml()


if __name__ == '__main__':
    main()
