from .cli import CLI


class SwiftCLI(CLI):

    def __init__(self, compiler=None):
        super(SwiftCLI, self).__init__('Swift', compiler, False)

    def setup_runner(self, args, enable_options, disable_options, runner):
        # super(SwiftCLI, self).setup_runner(args, list(set(enable_options)), disable_options, runner)
        runner.reset()
        runner.has_compiler_option_raw = self.has_compiler_option_raw
        runner.has_runtime_option_raw = self.has_runtime_option_raw
        runner.set_stdin(args.stdin)
        if self.has_runtime_option_raw:
            runner.set_runtime_options(args.runtime_options)
        runner.build_options(enable_options, disable_options, not args.no_default)
        options = args.sources + args.compile_options
        for x in options:
            if x.endswith('main.swift'):
                idx = options.index(x)
                del options[idx]
                options.extend([x, '-o', 'prog'])
        runner.build_compiler_options(options)


def swift(compiler=None):
    cli = SwiftCLI(compiler)
    cli.execute()


def main():
    swift()


if __name__ == '__main__':
    main()
