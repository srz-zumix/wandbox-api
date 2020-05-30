#!/usr/bin/env python
#
# cli.py
#

"""
Wandbox CLI for Python
"""

import wandbox

import argparse
import sys
import json

from .wandbox import Wandbox
from .runner import Runner
from argparse import ArgumentParser

VERSION = wandbox.__version__


def get_compiler_list(retry, wait):
    return Wandbox.Call(Wandbox.GetCompilerList, retry, wait)


class CLI:
    """wandbox CLI class"""

    def __init__(self, lang=None, compiler=None):
        self.setup(lang, compiler)

    def command_list(self, args):
        r = get_compiler_list(args.retry, args.retry_wait)
        if args.language:
            r = [x for x in r if args.language == x['language']]
        if args.compiler:
            r = [x for x in r if args.compiler == x['name']]
        print(json.dumps(r, indent=2))

    def command_lang(self, args):
        if args.language:
            print(args.language)
        else:
            r = get_compiler_list(args.retry, args.retry_wait)
            langs = map(lambda x: x['language'], r)
            print('\n'.join(sorted(set(langs))))

    def command_compiler(self, args):
        r = get_compiler_list(args.retry, args.retry_wait)
        for d in r:
            if args.language:
                if args.language == d['language']:
                    print(d['name'])
            else:
                print('{0}: {1}'.format(d['language'], d['name']))

    def format_indent(self, value, indent=0):
        return '{0}{1}'.format(' ' * indent, value)

    def format_default(self, name, indent=0):
        return '{0}{1} (default)'.format(' ' * indent, name)

    def command_options(self, args):
        r = get_compiler_list(args.retry, args.retry_wait)
        for d in r:
            prefix = ''
            indent = 0
            if args.language:
                if args.language != d['language']:
                    continue
            else:
                prefix = '{0}: '.format(d['language'])
            if args.compiler:
                if args.compiler != d['name']:
                    continue
            else:
                prefix = '{0}: '.format(d['name'])
                indent = 2
            if 'switches' in d:
                switches = d['switches']
                print(prefix)
                for s in switches:
                    if s['type'] == 'select':
                        default_option = s['default']
                        if 'name' in s:
                            print(self.format_indent(s['name'], indent))
                        else:
                            print(self.format_default(default_option, indent))
                        for o in s['options']:
                            if (o['name'] == default_option) and ('name' in s):
                                print(self.format_default(o['name'], indent + 2))
                            else:
                                print(self.format_indent(o['name'], indent + 2))
                    elif s['type'] == 'single':
                        if s['default']:
                            print(self.format_default(s['name'], indent))
                        else:
                            print(self.format_indent(s['name'], indent))

    def command_permlink(self, args):
        r = Wandbox.Call(lambda : Wandbox.GetPermlink(args.id[0]), args.retry, args.retry_wait)
        p = r['parameter']
        Runner.ShowParameter(p)
        print('result:')
        b = Runner.ShowResult(r['result'])
        sys.exit(b)

    def command_run(self, args):
        options = []
        for o in args.options:
            options.extend(o.split(','))
        self.run(args, options)

    def get_runner(self, args, options):
        return Runner(args.language, args.compiler, args.save, args.encoding, args.retry, args.retry_wait)

    def setup_runner(self, args, enable_options, disable_options, runner):
        runner.set_stdin(args.stdin)
        runner.set_runtime_options(args.runtime_options)
        runner.build_options(enable_options, disable_options, not args.no_default)
        runner.build_compiler_options(args.compile_options)

    def run(self, args, options):
        runner = self.get_runner(args, options)
        self.setup_runner(args, options, [], runner)
        self.run_with_runner(args, runner)

    def run_with_runner(self, args, runner):
        if args.dryrun:
            runner.dump()
            sys.exit(0)
        r = runner.run()
        b = Runner.ShowResult(r)
        sys.exit(b)

    def command_help(self, args):
        print(self.parser.parse_args([args.subcommand[0], '--help']))

    # command line option
    def setup(self, lang, compiler):
        self.parser = ArgumentParser()
        self.parser.add_argument(
            '-v',
            '--version',
            action='version',
            version=u'%(prog)s version ' + VERSION
        )
        self.parser.add_argument(
            '-l',
            '--language',
            default=lang,
            help=argparse.SUPPRESS if lang else 'specify language'
        )
        self.parser.add_argument(
            '-c',
            '--compiler',
            default=compiler,
            help=argparse.SUPPRESS if compiler else 'specify compiler'
        )
        self.parser.add_argument(
            '-x',
            '--options',
            action='append',
            default=[],
            help='used options for a compiler'
        )
        self.parser.add_argument(
            '-r',
            '--runtime-options',
            action='append',
            default=[],
            help='runtime options'
        )
        self.parser.add_argument(
            '-n',
            '--dryrun',
            action='store_true',
            help='dryrun'
        )
        self.parser.add_argument(
            '-s',
            '--save',
            action='store_true',
            help='generate permanent link.'
        )
        self.parser.add_argument(
            '--encoding',
            # default='utf-8-sig',
            help='set encoding'
        )
        self.parser.add_argument(
            '--no-default',
            action='store_true',
            help='no set default options'
        )
        self.parser.add_argument(
            '--stdin',
            help='set stdin'
        )
        self.parser.add_argument(
            '--retry-wait',
            type=int,
            default=30,
            metavar='SECONDS',
            help='wait time for retry when HTTPError occurs'
        )
        self.parser.add_argument(
            '--retry',
            type=int,
            default=1,
            metavar='COUNT',
            help='number of retries when HTTPError occurs'
        )
        subparser = self.parser.add_subparsers()

        list_cmd = subparser.add_parser(
            'list',
            description='show list api response',
            help='show list api response. see `list -h`'
        )
        list_cmd.set_defaults(handler=self.command_list)

        compiler_cmd = subparser.add_parser(
            'compiler',
            description='show support compilers',
            help='show support compilers. see `compiler -h`')
        compiler_cmd.set_defaults(handler=self.command_compiler)

        lang_cmd = subparser.add_parser(
            'lang',
            description='show support languages',
            help='show support languages. see `lang -h`'
        )
        lang_cmd.set_defaults(handler=self.command_lang)

        option_cmd = subparser.add_parser(
            'option',
            description='show compiler options',
            help='show compiler options. see `option -h`'
        )
        option_cmd.set_defaults(handler=self.command_options)

        permlink_cmd = subparser.add_parser(
            'permlink',
            description='get permlink',
            help='get permlink. see `permlink -h`'
        )
        permlink_cmd.set_defaults(handler=self.command_permlink)
        permlink_cmd.add_argument(
            'id',
            nargs=1,
            help='permlink id'
        )

        passthrough_cmd = subparser.add_parser(
            'run',
            prefix_chars='+',
            description='build and run command',
            help='build and run command. see `run +h`'
        )
        passthrough_cmd.set_defaults(handler=self.command_run)
        passthrough_cmd.add_argument(
            'compile_options',
            metavar='COMPILE_OPTIONS',
            nargs='*',
            help='comiple command options'
        )

        subcommands = self.parser.format_usage().split('{')[1].split('}')[0]
        help_cmd = subparser.add_parser('help', help='show subcommand help. see `help -h`')
        help_cmd.set_defaults(handler=self.command_help)
        help_cmd.add_argument(
            'subcommand',
            nargs=1,
            help='subcommand name {' + subcommands + '}'
        )
        help_cmd_default_usage = help_cmd.format_usage().replace('usage: ', '')
        help_cmd.usage = help_cmd_default_usage.replace('subcommand', 'subcommand{' + subcommands + '}')

    def parse_command_line(self):
        args = self.parser.parse_args()
        return args

    def print_help(self):
        self.parser.print_help()

    def execute(self):
        args = self.parse_command_line()
        if hasattr(args, 'handler'):
            args.handler(args)
        else:
            self.print_help()
