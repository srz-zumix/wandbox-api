#!/usr/bin/env python
#
# utils.py
#

"""
Utilities
"""

import glob
import os
import shlex


def case_insensitive_glob(path, pattern):
    name = ''.join(map(lambda c: '[{0}{1}]'.format(c.upper(), c.lower()) if c.isalpha() else c, pattern))
    return glob.glob(os.path.join(path, name))


def text_transform(value):
    try:
        if isinstance(value, str):
            return value.decode()
        # elif isinstance(value, unicode):
        #     return value.encode('utf_8')
    except Exception:  # nosec
        pass
    return value


def statements_quote(s):
    if s in ['(', ')', '{', '}']:
        return s
    else:
        return shlex.quote(s)


def statements_join(split_command):
    return " ".join([statements_quote(x) for x in split_command])


def split_statements(line, end_of_statement=";", commenters="#"):
    sl = shlex.shlex(line, posix=False)
    sl.commenters = commenters
    sl.source = None
    sl.wordchars += "!#$%&()*+,-./:;<=>?@[]^_{|}~".replace(end_of_statement, '')
    statements = []
    statement = []
    for s in sl:
        if s == end_of_statement:
            statements.append(" ".join(statement) + s)
            statement = []
        else:
            statement.append(s)
    if len(statement) > 0:
        statements.append(" ".join(statement))
    return statements
