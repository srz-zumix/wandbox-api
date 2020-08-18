import sys
import os
import wandbox
from wandbox import __cxx__ as cxx
from wandbox import __go__ as go

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

class test_wandbox_cxx(wandbox_test_base):

    def setUp(self):
        return super(test_wandbox_cxx, self).setUp()

    def tearDown(self):
        return super(test_wandbox_cxx, self).tearDown()

    def wandbox_cxx(self, opt):
        opt.extend(run_cxx_options)
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
            self.wandbox_cxx([ '--dryrun', '--no-warning', '--cpp-verbose', '--sprout', '--msgpack', '--optimize', '--cpp-pedantic', 'error', '--boost', '1.68.0' ])
        except SystemExit as e:
            self.assertEqual(e.code, 0)
            output = self.stdoout()
            eprint(output)
            self.assertTrue('cpp-verbose' in output)
            self.assertTrue('sprout' in output)
            self.assertTrue('msgpack' in output)
            self.assertTrue('optimize' in output)
            self.assertTrue('cpp-pedantic-errors' in output)
            self.assertTrue('boost-1.68.0-gcc-head' in output)
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


class test_wandbox_go(wandbox_test_base):

    def setUp(self):
        return super(test_wandbox_go, self).setUp()

    def tearDown(self):
        return super(test_wandbox_go, self).tearDown()

    def wandbox_go(self, opt):
        opt.extend(run_cxx_options)
        cli = go.GoCLI("go-head")
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


if __name__ == '__main__':
    test_loader = unittest.defaultTestLoader
    test_runner = unittest.TextTestRunner()
    test_suite = test_loader.discover('.')
    test_runner.run(test_suite)
