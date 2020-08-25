from .cli import CLI
from .__js__ import JsRunner


class TscCLI(CLI):

    def __init__(self, compiler=None):
        super(TscCLI, self).__init__('TypeScript', compiler, False)

    def get_runner(self, args, options):
        runner = JsRunner(args.language, args.compiler, args.save, args.encoding, args.retry, args.retry_wait)
        runner.configs.append('tsconfig.json')
        return runner


def ts(compiler=None):
    cli = TscCLI(compiler)
    cli.execute()


def main():
    ts()


if __name__ == '__main__':
    main()
