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

test_deps = ['importlib-metadata<2,>=0.12', 'tox', 'pytest']

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
        , "Programming Language :: Python :: 3.9"
    ]
    , entry_points={
        'console_scripts': [
            'wandbox          = wandbox.__main__:main',
            'wandbox-bash     = wandbox.__bash__:main',
            'wandbox-cc       = wandbox.__cc__:main',
            'wandbox-gcc      = wandbox.__cc__:gcc',
            'wandbox-clang    = wandbox.__cc__:clang',
            'wandbox-cxx      = wandbox.__cxx__:main',
            'wandbox-g++      = wandbox.__cxx__:gcc',
            'wandbox-clang++  = wandbox.__cxx__:clang',
            'wandbox-CPP      = wandbox.__cpp__:main',
            'wandbox-gcc-PP   = wandbox.__cpp__:gcc',
            'wandbox-clang-PP = wandbox.__cpp__:clang',
            'wandbox-coffee   = wandbox.__coffee__:main',
            'wandbox-crystal  = wandbox.__crystal__:main',
            'wandbox-cs       = wandbox.__csharp__:main',
            'wandbox-dmd      = wandbox.__dmd__:dmd',
            'wandbox-gdmd     = wandbox.__dmd__:gdmd',
            'wandbox-ldmd2    = wandbox.__dmd__:ldmd2',
            'wandbox-dub      = wandbox.__dub__:main',
            'wandbox-elixir   = wandbox.__elixir__:main',
            'wandbox-mix      = wandbox.__elixir__:mix',
            'wandbox-erlang   = wandbox.__erlang__:main',
            'wandbox-fsharpc  = wandbox.__fsharp__:main',
            'wandbox-ghc      = wandbox.__ghc__:main',
            'wandbox-stack    = wandbox.__ghc__:haskell_stack',
            'wandbox-go       = wandbox.__go__:main',
            'wandbox-java     = wandbox.__java__:main',
            'wandbox-js       = wandbox.__js__:main',
            'wandbox-node     = wandbox.__js__:node',
            'wandbox-spidermonkey = wandbox.__js__:spidermonkey',
            'wandbox-sbcl     = wandbox.__lisp__:main',
            'wandbox-clisp    = wandbox.__lisp__:clisp',
            'wandbox-lua      = wandbox.__lua__:main',
            'wandbox-luajit   = wandbox.__lua__:luajit',
            'wandbox-nim      = wandbox.__nim__:main',
            'wandbox-ocamlopt = wandbox.__ocaml__:main',
            'wandbox-fpc      = wandbox.__pascal__:main',
            'wandbox-perl     = wandbox.__perl__:main',
            'wandbox-php      = wandbox.__php__:main',
            'wandbox-python   = wandbox.__python__:main',
            'wandbox-python2  = wandbox.__python__:python2',
            'wandbox-python3  = wandbox.__python__:python3',
            'wandbox-pypy     = wandbox.__python__:pypy',
            'wandbox-ruby     = wandbox.__ruby__:main',
            'wandbox-mruby    = wandbox.__ruby__:mruby',
            'wandbox-swift    = wandbox.__swift__:main',
            'wandbox-tsc      = wandbox.__tsc__:main',
            'wandbox-ssl      = wandbox.__openssl__:main'
        ]
    }
    , install_requires=['requests', 'pyyaml']
    , tests_require=test_deps
    , test_suite="tests.test_suite"
    , extras_require={
        'test': test_deps
    }
)
