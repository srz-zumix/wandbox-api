# Wandbox API for Python

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/2ff3eb34b617416c97f590b45b5e82fe)](https://app.codacy.com/manual/srz-zumix/wandbox-api?utm_source=github.com&utm_medium=referral&utm_content=srz-zumix/wandbox-api&utm_campaign=Badge_Grade_Settings)

[Wandbox](http://melpon.org/wandbox/) is a social compilation service.  
This project is a Pythonic binding to the Wandbox API, and CLI command.

## Installation

```
  git clone https://github.com/srz-zumix/wandbox-api.git
  cd wandbox-api
  python setup.py install
```

## CLI

### wandbox

```
usage: wandbox [-h] [-v] [-c COMPILER] [-x OPTIONS] [-r RUNTIME_OPTIONS] [-n] [-s] [--encoding ENCODING]
               [--no-default] [--stdin STDIN] [--retry-wait SECONDS] [--retry COUNT]
               {list,compiler,lang,option,permlink,run,help} ...

positional arguments:
  {list,compiler,lang,option,permlink,run,help}
    list                show list api response. see `list -h`
    compiler            show support compilers. see `compiler -h`
    lang                show support languages. see `lang -h`
    option              see `option -h`
    permlink            get permlink. see `permlink -h`
    run                 build and run command. see `run -h`
    help                see `help -h`

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
```

### C++

* wandbox-cxx
* wandbox-g++  
  (wandbox-cxx -c gcc-head)
* wandbox-clang++  
  (wandbox-cxx -c clang-head)

```
usage: wandbox-cxx [-h] [-v] [-c COMPILER] [-x OPTIONS] [-r RUNTIME_OPTIONS] [-n] [-s] [--encoding ENCODING]
                   [--no-default] [--stdin STDIN] [--retry-wait SECONDS] [--retry COUNT] [--std VERSION]
                   [--boost VERSION] [--optimize] [--cpp-verbose] [--sprout] [--msgpack]
                   {list,compiler,lang,option,permlink,run,help} ...

positional arguments:
  {list,compiler,lang,option,permlink,run,help}
    list                show list api response. see `list -h`
    compiler            show support compilers. see `compiler -h`
    lang                show support languages. see `lang -h`
    option              see `option -h`
    permlink            get permlink. see `permlink -h`
    run                 build and run command. see `run -h`
    help                see `help -h`

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
  --optimize            use optimization
  --cpp-verbose         use cpp-verbose
  --sprout              use sprout
  --msgpack             use msgpack
```
