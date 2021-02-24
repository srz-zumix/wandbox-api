#
# Makefile


local:
	${CXX} sample.cpp test.cpp

wandbox:
	CXX="wandbox-g++     run" make -C . local --no-print-directory
	CXX="wandbox-clang++ run" make -C . local --no-print-directory
