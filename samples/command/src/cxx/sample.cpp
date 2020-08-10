// This file is a "Hello, world!" in C++ language by GCC for wandbox.
#include <iostream>
#include <cstdlib>
#include "test.h"

int main()
{
    std::cout << "Hello, Wandbox!" << std::endl;
#if defined(PRINT_MESSAGE)
    std::cout << PRINT_MESSAGE << std::endl;
#endif
    std::cout << test() << std::endl;
    return 0;
}
