Wandbox Python API
===========

[Wandbox](http://melpon.org/wandbox/) is a social compilation service.  
This project is a Pythonic binding to the Wandbox API.

Installation
--------------------------------------------------

```
  git clone https://github.com/srz-zumix/wandbox-api.git
  cd wandbox-api
  python setup.py install
```

Getting Started
--------------------------------------------------

```python
  from wandbox import Wandbox

  w = Wandbox()
  w.compiler('gcc-head')
  w.options('warning,gnu++1y')
  w.compiler_options('-Dx=hogefuga\n-O3')
  w.add_file("test.h", "int d=42;");
  w.code('#include <iostream>\n#include "test.h"\nint main() { int x = 0; std::cout << "hoge" << d << std::endl; }')
  print w.run()
```
