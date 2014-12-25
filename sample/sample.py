#!/usr/bin/env python

from wandbox import Wandbox

if __name__ == '__main__':
	w = Wandbox()
	w.compiler('gcc-head')
	w.options('warning,gnu++1y')
	w.compiler_options('-Dx=hogefuga\n-O3')
	w.code('#include <iostream>\nint main() { int x = 0; std::cout << "hoge" << std::endl; }')
	print w.run()

