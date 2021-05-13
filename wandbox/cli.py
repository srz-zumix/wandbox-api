#!/usr/bin/env python
#
# cli.py
#

"""
Wandbox CLI for Python
"""

import os
import sys
import json
import traceback
import fnmatch

from . import __version__ as VERSION
from .wandbox import Wandbox
from .runner import Runner
from .wrapper import Wrapper
from argparse import ArgumentParser
from argparse import SUPPRESS
from io import StringIO


class CLI:
    """wandbox CLI class"""

    def __init__(self, lang=None, compiler=None,
            has_option=True, has_compiler_option_raw=True, has_runtime_option_raw=True,
            run_prefix_chars='+'):
        self.wrapper = Wrapper()
        self.compiler_list = None
        self.result_key = None
        self.language = lang
        self.has_option = has_option
        self.has_compiler_option_raw = has_compiler_option_raw
        self.has_runtime_option_raw = has_runtime_option_raw
        self.run_prefix_chars = run_prefix_chars
        self.setup(lang, compiler, has_option)

    def command_list(self, args):
        r = self.get_compiler_list(args.retry, args.retry_wait)
        if args.language:
            r = [x for x in r if args.language == x['language']]
        if args.compiler:
            r = [x for x in r if fnmatch.fnmatch(x['name'], args.compiler)]
        print(json.dumps(r, indent=2))

    def command_lang(self, args):
        self.wrapper.languages(args.language, args.retry, args.retry_wait, args.verbose)

    def command_compiler(self, args):
        self.wrapper.compilers(args.language, args.compiler, args.retry, args.retry_wait, args.verbose)

    def command_options(self, args):
        self.wrapper.options(args.language, args.compiler, args.retry, args.retry_wait, args.verbose)

    def command_version(self, args):
        self.auto_setup_compiler(args)
        r = self.get_compiler_list(args.retry, args.retry_wait)
        compiler = self.wrapper.find_compiler(r, args.language, args.compiler)
        print(compiler['version'])

    def command_permlink(self, args):
        r = Wandbox.Call(lambda : Wandbox.GetPermlink(args.id[0]), args.retry, args.retry_wait)
        p = r['parameter']
        Wandbox.ShowParameter(p)
        print('result:')
        b = Wandbox.ShowResult(r['result'])
        sys.exit(b)

    def command_template(self, args):
        print(self.get_template_code(args))

    def command_run_template(self, args):
        setattr(args, 'sources', ['-'])
        sys.stdin = StringIO(self.get_template_code(args))
        options = []
        for o in args.options:
            options.extend(o.split(','))
        runner = self.get_runner(args, options)
        self.setup_runner(args, options, [], runner)
        self.run_with_runner(args, runner)

    def command_user(self, args):
        print(self.get_user(args))

    def command_run(self, args):
        options = []
        for o in args.options:
            options.extend(o.split(','))
        try:
            self.run(args, options)
        except Exception:
            print(traceback.format_exc())
            self.print_help()
            sys.exit(1)

    def get_runner(self, args, options):
        return Runner(args.language, args.compiler, args.save, args.encoding, args.retry, args.retry_wait)

    def setup_runner(self, args, enable_options, disable_options, runner):
        runner.reset()
        runner.has_compiler_option_raw = self.has_compiler_option_raw
        runner.has_runtime_option_raw = self.has_runtime_option_raw
        runner.set_stdin(args.stdin)
        if self.has_runtime_option_raw:
            runner.set_runtime_options(args.runtime_options)
        runner.build_options(enable_options, disable_options, not args.no_default)
        runner.build_compiler_options(args.sources + args.compile_options)

    def run(self, args, options):
        self.auto_setup_compiler(args)
        runner = self.get_runner(args, options)
        self.setup_runner(args, options, [], runner)
        self.run_with_runner(args, runner)

    def get_compiler_list(self, retry, wait):
        return self.wrapper.get_compiler_list(retry, wait)

    def auto_setup_compiler(self, args):
        l, c = self.wrapper.resolve_compiler(args.language, args.compiler, args.retry, args.retry_wait, args.no_head)
        if l:
            args.language = l
        if c:
            args.compiler = c

    def run_with_runner(self, args, runner):
        if args.dryrun:
            runner.dump()
            sys.exit(0)
        r = runner.run()
        exit_code = self.on_run_response(r)
        sys.exit(exit_code)

    def on_run_response(self, response):
        if self.result_key:
            exit_code, msg = Wandbox.GetResult(response, self.result_key)
            print(msg)
        else:
            exit_code = Wandbox.ShowResult(response)
        return exit_code

    def command_help(self, args):
        print(self.parser.parse_args([args.subcommand[0], '--help']))

    # command line option
    def setup(self, lang, compiler, has_option):
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
            help=SUPPRESS if lang else 'specify language'
        )
        self.parser.add_argument(
            '-c',
            '--compiler',
            default=compiler,
            help=SUPPRESS if compiler else
            'specify compiler (can use fnmatch, use first match compiler. e.g. clang-3.9.*[!c] => clang-3.9.1)'
        )
        self.parser.add_argument(
            '-x',
            '--options',
            action='append',
            default=[],
            help=SUPPRESS if not has_option else 'used options for a compiler'
        )
        if self.has_runtime_option_raw:
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
            '-V',
            '--verbose',
            action='store_true',
            help='verbose log'
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
            '--no-head',
            action='store_true',
            help='ignore head compiler version (at auto setup)'
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

        compilers_cmd = subparser.add_parser(
            'compilers',
            description='show support compilers',
            help='show support compilers. see `compilers -h`')
        versions_cmd = subparser.add_parser(
            'versions',
            description='show support compilers',
            help='show support compilers. see `versions -h`')
        compilers_cmds = [compilers_cmd, versions_cmd]
        for compiler_cmd_ in compilers_cmds:
            compiler_cmd_.set_defaults(handler=self.command_compiler)

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

        version_cmd = subparser.add_parser(
            'version',
            description='show compiler version from version-command',
            help='show compiler version from version-command. see `version -h`')
        version_cmd.set_defaults(handler=self.command_version)

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

        run_cmd = subparser.add_parser(
            'run',
            prefix_chars=self.run_prefix_chars,
            description='build and run command',
            help='build and run command. see `run {0}h`'.format(self.run_prefix_chars)
        )
        # build_cmd = subparser.add_parser(
        #     'build',
        #     prefix_chars=self.run_prefix_chars,
        #     description='build and run command (run command alias)',
        #     help='build and run command (run command alias). see `build {0}h`'.format(self.run_prefix_chars)
        # )
        passthrough_cmds = [run_cmd]
        for passthrough_cmd in passthrough_cmds:
            passthrough_cmd.set_defaults(handler=self.command_run)
            passthrough_cmd.add_argument(
                'sources',
                metavar='SOURCE',
                nargs='+',
                help='source files'
            )
            passthrough_cmd.add_argument(
                'compile_options',
                metavar='COMPILE_OPTIONS',
                nargs='*',
                help='comiple options'
            )

        template_cmd = subparser.add_parser(
            'template',
            description='get template code',
            help='get wandbox template code. see `template -h`'
        )
        template_cmd.set_defaults(handler=self.command_template)

        run_template_cmd = subparser.add_parser(
            'run-template',
            prefix_chars=self.run_prefix_chars,
            description='run wandbox template code',
            help='run wandbox template code. see `run-template {0}h`'.format(self.run_prefix_chars)
        )
        run_template_cmd.set_defaults(handler=self.command_run_template)
        run_template_cmd.add_argument(
            'compile_options',
            metavar='COMPILE_OPTIONS',
            nargs='*',
            help='comiple options'
        )

        user_cmd = subparser.add_parser(
            'user',
            description='get user info',
            help='get wandbox user info. see `user -h`'
        )
        user_cmd.set_defaults(handler=self.command_user)
        user_cmd.add_argument(
            'session',
            nargs=1,
            help='session key passed by Wandbox'
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

    def parse_command_line(self, argv):
        args = self.parser.parse_args(argv)
        if 'WANDBOX_DRYRUN' in os.environ:
            args.dryrun = True
        return args

    def print_help(self):
        self.parser.print_help()

    def execute(self):
        self.execute_with_args()

    def execute_with_args(self, args=None):
        args = self.parse_command_line(args)
        if hasattr(args, 'handler'):
            args.handler(args)
        else:
            self.print_help()

    def check_bool_option(self, args, name, enable_options, disable_options, prefix=''):
        attr_name = name.replace('-', '_')
        if name.startswith('no-'):
            opt_name = prefix + name.replace('no-', '')
            self._check_bool_option(args, opt_name, attr_name, disable_options)
        else:
            opt_name = prefix + name
            self._check_bool_option(args, opt_name, attr_name, enable_options)

    def _check_bool_option(self, args, opt_name, attr_name, options):
        if hasattr(args, attr_name):
            if getattr(args, attr_name):
                options.append(opt_name)

    def get_template_code(self, args):
        self.auto_setup_compiler(args)
        return self.wrapper.get_template_code(args.language, args.compiler, args.retry, args.retry_wait)

    def get_user(self, args):
        return self.wrapper.get_user(args.session, args.retry, args.retry_wait)
