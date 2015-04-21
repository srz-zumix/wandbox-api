#!/usr/bin/env python

from wandbox import Wandbox

if __name__ == '__main__':
	w = Wandbox()
	w.compiler('gcc-head')
	w.options('warning,gnu++1y')
	w.compiler_options('-Dx=hogefuga\n-O3')
	w.add_file("test.h", "int d=42;");
	w.code('#include <iostream>\n#include "test.h"\nint main() { int x = 0; std::cout << "hoge" << d << std::endl; }')
	print w.run()

