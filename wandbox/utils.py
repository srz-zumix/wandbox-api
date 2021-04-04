#!/usr/bin/env python
#
# utils.py
#

"""
Utilities
"""

import glob
import os


def case_insensitive_glob(path, pattern):
    name = ''.join(map(lambda c: '[{0}{1}]'.format(c.upper(), c.lower()) if c.isalpha() else c, pattern))
    return glob.glob(os.path.join(path, name))
