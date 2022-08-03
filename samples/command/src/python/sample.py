# This file is a "Hello, world!" in Python language by CPython for wandbox.

import test, test4
from test2 import hoge; from test2 import hoge2, hoge3
from test3 import fuga as FUGA
from subdir.test5 import test as Test

print("Hello, world!")
test.test()
hoge()
hoge2()
hoge3()
FUGA()
test4.piyo()
Test()

# CPython references:
#   https://www.python.org/
