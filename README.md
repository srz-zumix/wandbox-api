# Wandbox API for Python

[![PyPI version](https://badge.fury.io/py/wandbox-api.svg)](https://badge.fury.io/py/wandbox-api)
[![Python Versions](https://img.shields.io/pypi/pyversions/wandbox_api.svg)](https://pypi.org/project/wandbox-api/)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/2ff3eb34b617416c97f590b45b5e82fe)](https://app.codacy.com/manual/srz-zumix/wandbox-api?utm_source=github.com&utm_medium=referral&utm_content=srz-zumix/wandbox-api&utm_campaign=Badge_Grade_Settings)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/srz-zumix/wandbox-api.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/srz-zumix/wandbox-api/context:python)

[Wandbox](http://melpon.org/wandbox/) is a social compilation service.  
This project is a Pythonic binding to the Wandbox API, and CLI command.

## Installation

> pip install wandbox-api

## CLI

* [C++](#c)
* [C](#c-1)
* [CPP](#CPP)
* [GO](#Go)
* [Python](#Python)
* [Ruby](#Ruby)
* [OpenSSL](#OpenSSL)

### wandbox

```sh
usage: wandbox [-h] [-v] [-l LANGUAGE] [-c COMPILER] [-x OPTIONS] [-r RUNTIME_OPTIONS] [-n] [-s] [--encoding ENCODING]
               [--no-default] [--stdin STDIN] [--retry-wait SECONDS] [--retry COUNT]
               {list,compiler,versions,lang,option,permlink,run,help} ...

positional arguments:
  {list,compiler,versions,lang,option,permlink,run,help}
    list                show list api response. see `list -h`
    compiler            show support compilers. see `compiler -h`
    versions            show support compilers. see `versions -h`
    lang                show support languages. see `lang -h`
    option              show compiler options. see `option -h`
    permlink            get permlink. see `permlink -h`
    run                 build and run command. see `run +h`
    help                show subcommand help. see `help -h`

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -l LANGUAGE, --language LANGUAGE
                        specify language
  -c COMPILER, --compiler COMPILER
                        specify compiler
  -x OPTIONS, --options OPTIONS
                        used options for a compiler
  -r RUNTIME_OPTIONS, --runtime-options RUNTIME_OPTIONS
                        runtime options
  -n, --dryrun          dryrun
  -s, --save            generate permanent link.
  --encoding ENCODING   set encoding
  --no-default          no set default options
  --stdin STDIN         set stdin
  --retry-wait SECONDS  wait time for retry when HTTPError occurs
  --retry COUNT         number of retries when HTTPError occurs
```

### C++

Include files required for compilation are automatically added to the file list.

* wandbox-cxx
* wandbox-g++  
  (wandbox-cxx -c gcc-head)
* wandbox-clang++  
  (wandbox-cxx -c clang-head)

```sh
usage: wandbox-cxx [-h] [-v] [-c COMPILER] [-x OPTIONS] [-r RUNTIME_OPTIONS] [-n] [-s] [--encoding ENCODING]
                   [--no-default] [--stdin STDIN] [--retry-wait SECONDS] [--retry COUNT] [--std VERSION]
                   [--boost VERSION] [--no-warning] [--optimize] [--cpp-pedantic PEDANTIC] [--cpp-verbose] [--sprout] [--msgpack]
                   {list,compiler,versions,lang,option,permlink,run,help} ...

positional arguments:
  {list,compiler,versions,lang,option,permlink,run,help}
    list                show list api response. see `list -h`
    compiler            show support compilers. see `compiler -h`
    versions            show support compilers. see `versions -h`
    lang                show support languages. see `lang -h`
    option              show compiler options. see `option -h`
    permlink            get permlink. see `permlink -h`
    run                 build and run command. see `run +h`
    help                show subcommand help. see `help -h`

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -c COMPILER, --compiler COMPILER
                        specify compiler
  -x OPTIONS, --options OPTIONS
                        used options for a compiler
  -r RUNTIME_OPTIONS, --runtime-options RUNTIME_OPTIONS
                        runtime options
  -n, --dryrun          dryrun
  -s, --save            generate permanent link.
  --encoding ENCODING   set encoding
  --no-default          no set default options
  --stdin STDIN         set stdin
  --retry-wait SECONDS  wait time for retry when HTTPError occurs
  --retry COUNT         number of retries when HTTPError occurs
  --std VERSION         set --std options
  --boost VERSION       set boost options version X.XX or nothing
  --no-warning          disable warning option
  --optimize            use optimization
  --cpp-pedantic PEDANTIC
                        use cpp-pedantic
  --cpp-verbose         use cpp-verbose
  --sprout              use sprout
  --msgpack             use msgpack
```

#### C++ Example

> wandbox-cxx -c gcc-head run main.cpp -DWANDBOX

> CXX="wandbox-gcc run" make

### C

Include files required for compilation are automatically added to the file list.

* wandbox-cc
  (wandbox -l C)
* wandbox-gcc  
  (wandbox-cc -c gcc-head-c)
* wandbox-clang
  (wandbox-cc -c clang-head-c)

### CPP

Include files required for compilation are automatically added to the file list.

* wandbox-CPP
  (wandbox -l CPP)
* wandbox-gcc-PP  
  (wandbox-CPP -c gcc-head-pp)
* wandbox-clang-PP
  (wandbox-CPP -c clang-head-pp)

### Go

* wandbox-go
  (wandbox -l Go)

### Python

Import files/modules required for compilation are automatically added to the file list.

* wandbox-python
  (wandbox -l Python)
* wandbox-python2  
  (wandbox-cxx -c cpython-2.7-head)
* wandbox-python3  
  (wandbox-cxx -c cpython-head)
* wandbox-pypy
  (wandbox-cxx -c pypy-head)

#### Python Example

> wandbox-python3 run sample.py

wandbox-python supports setup.py

> wandbox-python -c cpython-head -r test run setup.py

If you open a file, add the file

> wandbox-python -c cpython-head -r test run setup.py README.md

### Ruby

Require files required for compilation are automatically added to the file list.

* wandbox-ruby
  (wandbox -l Ruby)
* wandbox-mruby  
  (wandbox-ruby -c mruby-head)

#### Ruby Example

> wandbox-ruby run sample.rb

### OpenSSL

Even just having wandbox would be enough.

* wandbox-ssl

#### OpenSSL Example

> wandbox-ssl genrsa -out test.key 2048
> wandbox-ssl rsa -in test.key -pubout -out test.key.pub
