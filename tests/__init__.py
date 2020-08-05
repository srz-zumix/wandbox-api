try:
    import unittest2 as unittest
except:
    import unittest
# import test_wandbox_api
import os

def test_suite():
    test_loader = unittest.TestLoader()
    # test_loader = unittest.defaultTestLoader
    test_suite = test_loader.discover('./tests')
    # test_suite = loader.loadTestsFromModule(test_wandbox_api)
    return test_suite
