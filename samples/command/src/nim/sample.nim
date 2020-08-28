# This file is a "Hello, world!" in Nim language for wandbox.

import test1
import test2, test3
import test4 except Hoge4
from test5 import Test5
import test6 except Hoge6, Fuga6
from test7 import Test7, Fuga7
import "subdir/test8"

echo "Hello, Wandbox!"
Test1()
Test2()
Test3()
Test4()
Fuga4()
Test5()
Test6()
Test7()
Fuga7()
Test8()

# Nim language references:
#   https://nim-lang.org/
#   https://nim-lang.org/docs/manual.html
