#
# Makefile


local:
	${CC} sample.c test.c

wandbox:
	CC="wandbox-gcc   run" make -C . local --no-print-directory
	CC="wandbox-clang run" make -C . local --no-print-directory
