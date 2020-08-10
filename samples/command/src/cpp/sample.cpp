// This file is a "Hello, world!" in CPP(C Preprocessor) by gcc for wandbox.
#if __has_include(<boost/preprocessor.hpp>)
#include <boost/preprocessor.hpp>
#endif
#include "test.h"

#define Hello 40
#define Wandbox 2

BOOST_PP_ADD(Hello, Wandbox)

// C Preprocessor references:
//   https://gcc.gnu.org/onlinedocs/cpp/
//   http://www.open-std.org/jtc1/sc22/wg21/

// Boost.Preprocessor reference:
//   http://www.boost.org/libs/preprocessor/
