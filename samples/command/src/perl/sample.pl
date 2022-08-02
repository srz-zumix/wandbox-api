# This file is a "Hello, world!" in Perl language for wandbox.
use FindBin;
use lib "$FindBin::Bin/subdir";

BEGIN {
  unshift @INC, "$FindBin::Bin/";
}

require test0;
require './test1.pl'; require test2;

print "Hello, Wandbox!\n";
test0();
test1();
test2();

# Perl language references:
#   http://perldoc.perl.org/
