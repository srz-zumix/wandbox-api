# Wandbox API for Python

[![PyPI version](https://badge.fury.io/py/wandbox-api.svg)](https://badge.fury.io/py/wandbox-api)
[![Python Versions](https://img.shields.io/pypi/pyversions/wandbox_api.svg)](https://pypi.org/project/wandbox-api/)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/2ff3eb34b617416c97f590b45b5e82fe)](https://app.codacy.com/manual/srz-zumix/wandbox-api?utm_source=github.com&utm_medium=referral&utm_content=srz-zumix/wandbox-api&utm_campaign=Badge_Grade_Settings)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/srz-zumix/wandbox-api.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/srz-zumix/wandbox-api/context:python)
[![GitHub Actions](https://github.com/srz-zumix/wandbox-api/actions/workflows/main.yml/badge.svg)](https://github.com/srz-zumix/wandbox-api/actions/workflows/main.yml)

[Wandbox](http://melpon.org/wandbox/) is a social compilation service.  
This project is a Pythonic binding to the Wandbox API, and CLI command.

## Installation

> pip install wandbox-api

## CLI

[wandbox](#wandbox)

### for Languages

|                               |                           |                           |                     |                     |
|:------------------------------|:--------------------------|:--------------------------|:--------------------|:--------------------|
| [Bash](#Bash)                 | [C](#C)                   | [C#](#C-1)                | [C++](#C-2)         | [CMake](#CMake)     |
| [CoffeeScript](#CoffeeScript) | [CPP](#CPP)               | [Crystal](#Crystal)       | [D](#D)             | [Elixir](#Elixir)   |
| [Erlang](#Erlang)             | [F#](#F)                  | [Go](#Go)                 | [Groovy](#Groovy)   | [Haskell](#Haskell) |
| [Java](#Java)                 | [JavaScript](#JavaScript) | [Julia](#Julia)           | [Lazy K](#Lazy-K)   | [Lisp](#Lisp)       |
| [Lua](#Lua)                   | [Nim](#Nim)               | [OCaml](#OCaml)           | [OpenSSL](#OpenSSL) | [Pascal](#Pascal)   |
| [Perl](#Perl)                 | [PHP](#PHP)               | [Pony](#Pony)             | [Python](#Python)   | [R](#R)             |
| [Rill](#Rill)                 | [Ruby](#Ruby)             | [Rust](#Rust)             | [Scala](#Scala)     | [SQL](#SQL)         |
| [Swift](#Swift)               | [TypeScript](#TypeScript) | [Vim script](#Vim-script) |||

### wandbox

```sh
usage: wandbox [-h] [-v] [-l LANGUAGE] [-c COMPILER] [-x OPTIONS] [-r RUNTIME_OPTIONS] [-n] [-s] [--encoding ENCODING]
               [--no-default] [--stdin STDIN] [--retry-wait SECONDS] [--retry COUNT]
               {list,compilers,versions,lang,option,permlink,run,template,run-template,user,help} ...

positional arguments:
  {list,compilers,versions,lang,option,permlink,run,help}
    list                show list api response. see `list -h`
    compilers           show support compilers. see `compilers -h`
    versions            show support compilers. see `versions -h`
    lang                show support languages. see `lang -h`
    option              show compiler options. see `option -h`
    version             show compiler version from version-command. see `version -h`
    permlink            get permlink. see `permlink -h`
    run                 build and run command. see `run +h`
    template            get wandbox template code. see `template -h`
    run-template        run wandbox template code. see `run-template +h`
    user                get wandbox user info. see `user -h`
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
  -V, --verbose         verbose log
  -s, --save            generate permanent link.
  --encoding ENCODING   set encoding
  --no-head             ignore head compiler version (at auto setup)
  --no-default          no set default options
  --stdin STDIN         set stdin
  --retry-wait SECONDS  wait time for retry when HTTPError occurs
  --retry COUNT         number of retries when HTTPError occurs
```

----

### Bash

Source files required for runtime are automatically added to the file list.

* wandbox-bash

#### Bash Example

[Bash Example](./samples/command/src/bash)

----

### C

Include files required for compilation are automatically added to the file list.

* wandbox-cc  
  (wandbox -l C)
* wandbox-gcc  
  (wandbox -l C -c gcc-*-c)
* wandbox-clang  
  (wandbox -l C -c clang-*-c)

#### C Example

[C Example](./samples/command/src/cc)

----

### C#

* wandbox-cs  
  (wandbox -l C#)

#### C# Example

[C# Example](./samples/command/src/csharp)

----

### C++

Include files required for compilation are automatically added to the file list.

* wandbox-cxx  
  (wandbox -l C++)
* wandbox-g++  
  (wandbox -l C++ -c gcc-*)
* wandbox-clang++  
  (wandbox -l C++ -c clang-*)

```sh
usage: wandbox-cxx [-h] [-v] [-c COMPILER] [-x OPTIONS] [-r RUNTIME_OPTIONS] [-n] [-s] [--encoding ENCODING]
                   [--no-default] [--stdin STDIN] [--retry-wait SECONDS] [--retry COUNT] [--std VERSION]
                   [--boost VERSION] [--no-warning] [--optimize] [--cpp-pedantic PEDANTIC] [--cpp-verbose] [--sprout] [--msgpack]
                   {list,compilers,versions,lang,option,permlink,run,template,run-template,user,help} ...

positional arguments:
  {list,compilers,versions,lang,option,permlink,run,help}
    list                show list api response. see `list -h`
    compilers           show support compilers. see `compilers -h`
    versions            show support compilers. see `versions -h`
    lang                show support languages. see `lang -h`
    option              show compiler options. see `option -h`
    version             show compiler version from version-command. see `version -h`
    permlink            get permlink. see `permlink -h`
    run                 build and run command. see `run +h`
    template            get wandbox template code. see `template -h`
    run-template        run wandbox template code. see `run-template +h`
    user                get wandbox user info. see `user -h`
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
  -V, --verbose         verbose log
  -s, --save            generate permanent link.
  --encoding ENCODING   set encoding
  --no-head             ignore head compiler version (at auto setup)
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

[C++ Example](./samples/command/src/cxx)

----

### CMake

Include files are automatically added to the file list.

* wandbox-cmake  
  (wandbox -l CMake)

#### CMake Example

[CMake Example](./samples/command/src/cmake)

----

### CoffeeScript

* wandbox-coffee  
  (wandbox -l CoffeeScript)

#### CoffeeScript Example

[CoffeeScript Example](./samples/command/src/coffee)

----

### CPP

Include files required for compilation are automatically added to the file list.

* wandbox-CPP  
  (wandbox -l CPP)
* wandbox-gcc-PP  
  (wandbox -l CPP -c gcc-*-pp)
* wandbox-clang-PP  
  (wandbox -l CPP -c clang-*-pp)

#### CPP Example

[CPP Example](./samples/command/src/cpp)

----

### Crystal

Import modules required for compilation are automatically added to the file list.

* wandbox-crystal  
  (wandbox -l Crystal)

#### Crystal Example

[Crystal Example](./samples/command/src/crystal)

----

### D

* wandbox-dmd  
  (wandbox -l D -c dmd-*)
* wandbox-gdmd  
  (wandbox -l D -c gdc-*)
* wandbox-ldmd2  
  (wandbox -l D -c ldc-*)
* wandbox-dub

#### D Example

[D Example](./samples/command/src/dmd)
[Dub Example](./samples/command/src/dub)

----

### Elixir

* wandbox-elixir  
  (wandbox -l Elixir)
* wandbox-mix (Experimental)

#### Elixir Example

[Elixir Example](./samples/command/src/elixir)

----

### Erlang

* wandbox-erlang  
  (wandbox -l Erlang)

#### Erlang Example

[Erlang Example](./samples/command/src/erlang)

----

### F#

* wandbox-fsharpc  
  (wandbox -l F#)

#### F# Example

[F# Example](./samples/command/src/fsharp)

----

### Go

* wandbox-go  
  (wandbox -l Go)

#### Go Example

[Go Example](./samples/command/src/go)

----

### Groovy

* wandbox-groovy  
  (wandbox -l Groovy)

#### Groovy Example

[Groovy Example](./samples/command/src/groovy)

----

### Haskell

* wandbox-ghc  
  (wandbox -l Haskell)
* wandbox-stack

Note: wandbox-ghc/wandbox-stack add -dynamic compiler option. (output file size workarround.)

#### Haskell Example

[Haskell Example](./samples/command/src/haskell)

[Haskell Stack Example](./samples/command/src/haskell-stack)

----

### Java

* wandbox-java  
  (wandbox -l Java)

#### Java Example

[Java Example](./samples/command/src/java)

----

### JavaScript

Import files/modules required for runtime are automatically added to the file list.

* wandbox-js  
  (wandbox -l JavaScript)
* wandbox-node  
  (wandbox -l JavaScript-c nodejs-*)
* wandbox-spidermonkey  
  (wandbox -l JavaScript -c spidermonkey-*)

#### JavaScript Example

[JavaScript Example](./samples/command/src/js)

----

### Julia

* wandbox-julia  
  (wandbox -l Julia)

#### Julia Example

[Julia Example](./samples/command/src/julia)

----

### Lazy K

* wandbox-lazyk  
  (wandbox -l "Lazy K")

#### Lazy K Example

[Lazy K Example](./samples/command/src/lazyk)

----

### Lisp

* wandbox-sbcl  
  (wandbox -l Lisp)
* wandbox-clisp  
  (wandbox -l Lisp -c clisp-*)

#### Lisp Example

[Lisp Example](./samples/command/src/lisp)

----

### Lua

Import files/modules required for compilation are automatically added to the file list.

* wandbox-lua  
  (wandbox -l Lua)
* wandbox-luajit  
  (wandbox -l Lua -c luajit-*)

#### Lua Example

[Lua Example](./samples/command/src/lua)

----

### Nim

Import modules required for compilation are automatically added to the file list.

* wandbox-nim  
  (wandbox -l Nim)

#### Nim Example

[Nim Example](./samples/command/src/nim)

----

### OCaml

* wandbox-ocamlopt  
  (wandbox -l OCaml)

#### OCaml Example

[OCaml Example](./samples/command/src/ocaml)

----

### OpenSSL

Even just having wandbox would be enough.

* wandbox-ssl

#### OpenSSL Example

> wandbox-ssl genrsa -out test.key 2048

> wandbox-ssl rsa -in test.key -pubout -out test.key.pub

[OpenSSL Example](./samples/command/src/openssl)

----

### Pascal

Include files required for runtime are automatically added to the file list.

* wandbox-fpc  
  (wandbox -l Pascal)

#### Pascal Example

[Pascal Example](./samples/command/src/pascal)

----

### Perl

Require files/modules required for runtime are automatically added to the file list.

* wandbox-perl  
  (wandbox -l Perl)

#### Perl Example

[Perl Example](./samples/command/src/perl)

----

### PHP

Require/Include files required for runtime are automatically added to the file list.

* wandbox-php  
  (wandbox -l PHP)

#### PHP Example

[PHP Example](./samples/command/src/php)

----

### Pony

Build directory files are automatically added to the file list.

* wandbox-ponyc  
  (wandbox -l Pony)

#### Pony Example

> wandbox-ponyc run ./sample ./sample2

wandbox-ponyc builds ./sample and ./sample2, Then execute ./sample2

[Pony Example](./samples/command/src/pony)

----

### Python

Import files/modules required for runtime are automatically added to the file list.

* wandbox-python  
  (wandbox -l Python)
* wandbox-python2  
  (wandbox -l Python -c cpython-2.7-*)
* wandbox-python3  
  (wandbox -l Python -c cpython-*)
* wandbox-pypy  
  (wandbox -l Python -c pypy-*)

#### Python Example

> wandbox-python3 run sample.py

wandbox-python supports setup.py

> wandbox-python -c cpython-head -r test run setup.py

If you open a file, add the file

> wandbox-python -c cpython-head -r test run setup.py README.md

[Python Example](./samples/command/src/python)

----

### R

Source files are automatically added to the file list.

* wandbox-rscript  
  (wandbox -l R)

#### R Example

[R Example](./samples/command/src/r)

----

### Rill

* wandbox-rillc  
  (wandbox -l Rill)

#### Rill Example

[Rill Example](./samples/command/src/rill)

----

### Ruby

Require files required for runtime are automatically added to the file list.

* wandbox-ruby  
  (wandbox -l Ruby)
* wandbox-mruby  
  (wandbox -l Ruby -c mruby-*)

#### Ruby Example

> wandbox-ruby run sample.rb

[Ruby Example](./samples/command/src/ruby)

----

### Rust

Module files required for runtime are automatically added to the file list.

* wandbox-rustc  
  (wandbox -l Rust)
* wandbox-cargo

#### Rust Example

> wandbox-cargo run

[Rust Example](./samples/command/src/rust)

----

### Scala

* wandbox-scalac  
  (wandbox -l Scala)

#### Scala Example

> wandbox-scalac run *.scala

[Scala Example](./samples/command/src/scala)

----

### SQL

* wandbox-sqlite  
  (wandbox -l SQL)
* wandbox-sqlite3  
  (wandbox -l SQL)

#### SQL Example

> wandbox-sqlite3 run SELECT 'Hello, Wandbox!';

[SQL Example](./samples/command/src/sql)

----

### Swift

* wandbox-swift  
  (wandbox -l Swift)

#### Swift Example

> wandbox-swift run main.swift

[Swift Example](./samples/command/src/swift)

----

### TypeScript

Import files/modules required for compilation are automatically added to the file list.

* wandbox-tsc  
  (wandbox -l TypeScript)

#### TypeScript Example

[TypeScript Example](./samples/command/src/ts)

----

### Vim script

* wandbox-vim  
  (wandbox -l "Vim script")

#### Vim script Example

[Vim script Example](./samples/command/src/vim)

----

## CONTRIBUTING

[CONTRIBUTING](./CONTRIBUTING.md)
