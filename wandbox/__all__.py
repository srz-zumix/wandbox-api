from wandbox import __bash__ as bash
from wandbox import __cc__ as cc
from wandbox import __cmake__ as cmake
from wandbox import __coffee__ as coffee
from wandbox import __cpp__ as cpp
from wandbox import __crystal__ as crystal
from wandbox import __csharp__ as cs
from wandbox import __cxx__ as cxx
from wandbox import __dmd__ as dmd
from wandbox import __elixir__ as elixir
from wandbox import __erlang__ as erlang
from wandbox import __fsharp__ as fs
from wandbox import __ghc__ as ghc
from wandbox import __go__ as go
from wandbox import __groovy__ as groovy
from wandbox import __java__ as java
from wandbox import __js__ as js
from wandbox import __julia__ as julia
from wandbox import __lazyk__ as lazyk
from wandbox import __lisp__ as lisp
from wandbox import __lua__ as lua
from wandbox import __nim__ as nim
from wandbox import __ocaml__ as ocaml
from wandbox import __openssl__ as openssl
from wandbox import __pascal__ as pascal
from wandbox import __perl__ as perl
from wandbox import __php__ as php
from wandbox import __pony__ as pony
from wandbox import __python__ as python
from wandbox import __r__ as rscript
from wandbox import __ruby__ as ruby
from wandbox import __rust__ as rust
from wandbox import __scala__ as scala
from wandbox import __sql__ as sql
from wandbox import __swift__ as swift
from wandbox import __tsc__ as tsc
from wandbox import __vim__ as vim


def get_all_cli():
    clis = [
        bash.BashCLI.InnerCLI(),
        cc.CcCLI(),
        cmake.CMakeCLI(),
        coffee.CoffeeCLI(),
        cpp.CppCLI(),
        crystal.CrystalCLI(),
        cs.CsCLI(),
        cxx.CxxCLI(),
        dmd.DCLI(),
        elixir.ElixirCLI(),
        erlang.ErlangCLI(),
        fs.FsCLI(),
        ghc.GhcCLI(),
        go.GoCLI(),
        groovy.GroovyCLI(),
        java.JavaCLI(),
        js.JsCLI(),
        julia.JuliaCLI(),
        lazyk.LazyKCLI(),
        lisp.LispCLI(),
        lua.LuaCLI(),
        nim.NimCLI(),
        ocaml.OCamlCLI(),
        openssl.OpenSSLCLI.InnerCLI(),
        pascal.PascalCLI(),
        perl.PerlCLI(),
        php.PhpCLI(),
        pony.PonyCLI(),
        python.PythonCLI(),
        rscript.RscriptCLI(),
        ruby.RubyCLI(),
        rust.RustCLI(),
        scala.ScalaCLI(),
        sql.SqlCLI(),
        swift.SwiftCLI(),
        tsc.TscCLI(),
        vim.VimCLI()
    ]
    return clis
