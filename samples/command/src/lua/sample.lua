-- This file is a "Hello, world!" in Lua language for wandbox.

print "Hello, Wandbox!"

md01 = require("m1");
md01:print();

md02 = loadfile("m2.lua");
md02();

md03 = require "m3";
md03:print();

-- Lua language references:
--   https://www.lua.org/
