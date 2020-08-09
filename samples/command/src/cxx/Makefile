#
# Makefile


local:
	${CXX} sample.cpp test.cpp

wandbox:
	CXX="wandbox-cxx -c gcc-head run" make -C . local --no-print-directory
