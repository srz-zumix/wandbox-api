from .wandbox import Wandbox

import argparse
import sys

def main():
    with Wandbox() as w:
        w.compiler('gcc-head')
        w.options('warning,gnu++1y')
        w.compiler_options('-Dx=hogefuga\n-O3')
        w.code('#include <iostream>\nint main() { int x = 0; std::cout << "hoge" << std::endl; }')
        print(w.run())

if __name__ == '__main__':
    main()