# This file is a "Hello, world!" in Julia language for wandbox.

include("test1.jl"); include("test2.jl");

using .Test1
using .Test2

println("Hello, Wandbox!")

Test1.test()
Test2.test()

# Julia language references:
#   https://docs.julialang.org/en/v1/
