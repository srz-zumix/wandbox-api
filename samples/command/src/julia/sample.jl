# This file is a "Hello, world!" in Julia language for wandbox.

include("test1.jl")

using .Test1

println("Hello, Wandbox!")

Test1.test()

# Julia language references:
#   https://docs.julialang.org/en/v1/
