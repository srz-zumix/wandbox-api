from .cli import CLI


class DubRunner(Runner):

    def __init__(self, lang, compiler, save, encoding, retry, retry_wait, prefix_chars='-'):
        super(DubRunner, self).__init__(lang, compiler, save, encoding, retry, retry_wait, prefix_chars)

    def reset(self):
        pass

class DubCLI(CLI):

    def __init__(self, compiler=None):
        super(DubCLI, self).__init__('D', compiler, False)

    def get_runner(self, args, options):
        return DubRunner(args.language, args.compiler, args.save, args.encoding, args.retry, args.retry_wait)


def dub(compiler=None):
    cli = DubCLI(compiler)
    cli.execute()


def main():
    dmd()


if __name__ == '__main__':
    main()
