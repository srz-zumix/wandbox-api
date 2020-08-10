import sys
import os
import wandbox
from wandbox import __cxx__ as cxx

try:
    import unittest2 as unittest
except:
    import unittest

from unittest.mock import patch

src_path = 'samples/command/src'

class test_wandbox_cxx(unittest.TestCase):

    def setUp(self):
        return super(test_wandbox_cxx, self).setUp()

    def tearDown(self):
        return super(test_wandbox_cxx, self).tearDown()

    def test_build(self):
        try:
            with patch('argparse._sys.argv', [ __file__, 'run', os.path.join(src_path, 'cxx/sample.cpp'), os.path.join(src_path, 'cxx/test.cpp'), '-I' + os.path.join(src_path, 'cxx')]):
                cli = cxx.CxxCLI("gcc-head")
                cli.execute()
        except SystemExit as e:
            self.assertEqual(e.code, 0)
        else:
            self.fail('SystemExit exception expected')


if __name__ == '__main__':
    test_loader = unittest.defaultTestLoader
    test_runner = unittest.TextTestRunner()
    test_suite = test_loader.discover('.')
    test_runner.run(test_suite)
