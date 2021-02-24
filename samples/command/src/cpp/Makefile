#
# Makefile

local:
	${CXX} -CC -nostdinc -E -P sample.cpp test.cpp

wandbox:
	CXX="wandbox-gcc-PP   --boost 1.70 run" make -C . local --no-print-directory
	CXX="wandbox-clang-PP --boost 1.70 run" make -C . local --no-print-directory
