import sys
import os
# import json
import wandbox
from wandbox import Wandbox
from wandbox import cli as wandbox_cli
from wandbox import __cxx__ as cxx
from wandbox import __go__ as go
from wandbox.__all__ import get_all_cli
from wandbox.utils  import split_statements

try:
    import unittest2 as unittest
except:
    import unittest

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


src_path = 'samples/command/src'


class wandbox_test_base(unittest.TestCase):

    def setUp(self):
        self.capture = StringIO()
        sys.stdout = self.capture
        return super(wandbox_test_base, self).setUp()

    def tearDown(self):
        sys.stdout = sys.__stdout__
        self.capture.close()
        return super(wandbox_test_base, self).tearDown()

    def stdoout(self):
        value = self.capture.getvalue()
        return value

run_cxx_options = ['run', os.path.join(src_path, 'cxx/sample.cpp'), os.path.join(src_path, 'cxx/test.cpp'), '-I' + os.path.join(src_path, 'cxx')]

class test_wandbox_cli(wandbox_test_base):

    def setUp(self):
        return super(test_wandbox_cli, self).setUp()

    def tearDown(self):
        return super(test_wandbox_cli, self).tearDown()

    def wandbox_run(self, opt):
        cli = wandbox_cli.CLI()
        eprint(opt)
        cli.execute_with_args(opt)

    def test_wildcard(self):
        try:
            opt = [ '--dryrun', '--compiler=clang-11.*[!c]' ]
            opt.extend(run_cxx_options)
            self.wandbox_run(opt)
        except SystemExit as e:
            output = self.stdoout()
            eprint(output)
            self.assertEqual(e.code, 0)
            self.assertTrue('clang-11.1.0' in output)
        else:
            self.fail('SystemExit exception expected')

    def test_version(self):
        opt = [ '-l=C++', '-c=clang-11.1.0', 'version' ]
        self.wandbox_run(opt)
        output = self.stdoout()
        eprint(output)
        self.assertEqual('11.1.0', output.strip())

class test_wandbox_cxx(wandbox_test_base):

    def setUp(self):
        return super(test_wandbox_cxx, self).setUp()

    def tearDown(self):
        return super(test_wandbox_cxx, self).tearDown()

    def wandbox_cxx(self, opt, extend_opts=run_cxx_options):
        opt.extend(extend_opts)
        cli = cxx.CxxCLI("gcc-head")
        cli.execute_with_args(opt)

    def test_build(self):
        try:
            self.wandbox_cxx([])
        except SystemExit as e:
            self.assertEqual(e.code, 0)
        else:
            self.fail('SystemExit exception expected')

    def test_bool_options(self):
        try:
            self.wandbox_cxx([ '--dryrun', '--no-warning', '--cpp-verbose', '--sprout', '--msgpack', '--optimize', '--cpp-pedantic', 'error', '--boost', '1.78.0' ])
        except SystemExit as e:
            self.assertEqual(e.code, 0)
            output = self.stdoout()
            eprint(output)
            self.assertTrue('cpp-verbose' in output)
            self.assertTrue('sprout' in output)
            self.assertTrue('msgpack' in output)
            self.assertTrue('optimize' in output)
            self.assertTrue('cpp-pedantic-errors' in output)
            self.assertTrue('boost-1.78.0-gcc-head' in output)
            self.assertTrue('cpp-no-pedantic' not in output)
            self.assertTrue('warning' not in output)
        else:
            self.fail('SystemExit exception expected')

    def test_default_options(self):
        try:
            self.wandbox_cxx([ '--dryrun' ])
        except SystemExit as e:
            self.assertEqual(e.code, 0)
            output = self.stdoout()
            eprint(output)
            self.assertTrue('warning' in output)
        else:
            self.fail('SystemExit exception expected')

    def test_run_template(self):
        try:
            self.wandbox_cxx([ '--dryrun' ], ['run-template'])
        except SystemExit as e:
            self.assertEqual(e.code, 0)
            output = self.stdoout()
            eprint(output)
            self.assertTrue('Hello, Wandbox!' in output)
        else:
            self.fail('SystemExit exception expected')


class test_wandbox_go(wandbox_test_base):

    def setUp(self):
        return super(test_wandbox_go, self).setUp()

    def tearDown(self):
        return super(test_wandbox_go, self).tearDown()

    def wandbox_go(self, opt):
        opt.extend(run_cxx_options)
        cli = go.GoCLI("go-*")
        cli.execute_with_args(opt)

    def test_prefix_options(self):
        try:
            self.wandbox_go([ '--dryrun', '--gcflags-m' ])
        except SystemExit as e:
            self.assertEqual(e.code, 0)
            output = self.stdoout()
            eprint(output)
            self.assertTrue('go-gcflags-m' in output)
        else:
            self.fail('SystemExit exception expected')


class test_wandbox_options(wandbox_test_base):
    list_json = None

    @classmethod
    def setUpClass(cls):
        cls.list_json = Wandbox.GetCompilerList()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_options_config(self):
        l = test_wandbox_options.list_json
        clis = get_all_cli()
        for cli in clis:
            with self.subTest(cli=cli):
                ll = [x for x in l if cli.language == x['language']]
                if len(ll) > 0:
                    head = ll[0]
                    # print(json.dumps(head, indent=2))
                    self.assertEqual(cli.has_compiler_option_raw, head['compiler-option-raw'], cli.language)
                    # self.assertEqual(cli.has_runtime_option_raw, head['runtime-option-raw'], cli.language)
                    self.assertEqual(cli.has_runtime_option_raw, cli.language != "OpenSSL", cli.language)
                    self.assertEqual(cli.has_option, len(head['switches']) != 0, cli.language)


class test_wandbox_uitilities(wandbox_test_base):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_split_statements(self):
        statements = split_statements(". test.sh; source \"test data.sh\"")
        self.assertEqual(2, len(statements))
        self.assertEqual(". test.sh;", statements[0])
        self.assertEqual("source \"test data.sh\"", statements[1])

    def test_split_statements_2(self):
        statements = split_statements("include(\"test1.jl\");; include(\"test2.jl\");")
        self.assertEqual(3, len(statements))
        self.assertEqual("include(\"test1.jl\");", statements[0])
        self.assertEqual(";", statements[1])
        self.assertEqual("include(\"test2.jl\");", statements[2])


if __name__ == '__main__':
    test_loader = unittest.defaultTestLoader
    test_runner = unittest.TextTestRunner()
    test_suite = test_loader.discover('.')
    test_runner.run(test_suite)
