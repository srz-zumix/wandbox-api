#
# Makefile

local:
	${CXX} -CC -nostdinc -E -P sample.cpp test.cpp

wandbox:
	CXX="wandbox-gcc-PP run" make -C . local --no-print-directory
