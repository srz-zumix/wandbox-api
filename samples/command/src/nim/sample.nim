# This file is a "Hello, world!" in Nim language for wandbox.

import test1
import test2, test3
import test4 except Hoge4
from test5 import Test5
import test6 except Hoge6, Fuga6
from test7 import Test7, Fuga7
import "subdir/test8"
from test9_1 import Test9_1; import test9_2;


{.push header:"c/testA.c".} # push test

proc c_test1*()
proc c_test2*()

{.pop.}

proc c_test3*(){.header:"c/testB.c"};

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
Test9_1()
Test9_2()

c_test1()
c_test2()
c_test3()

# Nim language references:
#   https://nim-lang.org/
#   https://nim-lang.org/docs/manual.html
