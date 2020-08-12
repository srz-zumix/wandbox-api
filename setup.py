import os
import re
from setuptools import setup

f = open(os.path.join(os.path.dirname(__file__), 'README.md'))
readme = f.read()
f.close()

f = open(os.path.join(os.path.dirname(__file__), 'wandbox/__init__.py'))
for line in f:
    if '__version__ = ' in line:
        version_ = [x for x in re.split(r"[ =']", line) if x][1]
    elif '__author__ = ' in line:
        author_ = [x for x in re.split(r"[ =']", line) if x][1]
f.close()

setup(
    name = "wandbox-api"
    , version = version_
    , author = author_
    , author_email = "zumix.cpp@gmail.com"
    , url = "https://github.com/srz-zumix/wandbox-api/"
    , description = "A Python binding to the Wandbox API."
    , license = "MIT"
    , platforms = ["any"]
    , keywords = "API, Wandbox"
    , packages = ['wandbox']
    , long_description = readme
    , long_description_content_type='text/markdown'
    , classifiers = [
        "Development Status :: 4 - Beta"
        , "Topic :: Utilities"
        , "License :: OSI Approved :: MIT License"
        , "Programming Language :: Python"
        , "Programming Language :: Python :: 3.7"
        , "Programming Language :: Python :: 3.8"
    ]
    , entry_points={
        'console_scripts': [
            'wandbox     = wandbox.__main__:main',
            'wandbox-cc  = wandbox.__cc__:main',
            'wandbox-gcc = wandbox.__cc__:gcc',
            'wandbox-clang = wandbox.__cc__:clang',
            'wandbox-cxx = wandbox.__cxx__:main',
            'wandbox-g++ = wandbox.__cxx__:gcc',
            'wandbox-clang++ = wandbox.__cxx__:clang',
            'wandbox-CPP = wandbox.__cpp__:main',
            'wandbox-gcc-PP = wandbox.__cpp__:gcc',
            'wandbox-clang-PP = wandbox.__cpp__:clang',
            'wandbox-cs = wandbox.__csharp__:main',
            'wandbox-python = wandbox.__python__:main',
            'wandbox-python2 = wandbox.__python__:python2',
            'wandbox-python3 = wandbox.__python__:python3',
            'wandbox-pypy = wandbox.__python__:pypy'
        ]
    }
    , install_requires=['requests']
    , tests_require=['tox', 'pytest']
    , test_suite="tests.test_suite"
)
