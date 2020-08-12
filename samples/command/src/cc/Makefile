#
# Makefile


local:
	${CC} sample.c test.c

wandbox:
	CC="wandbox-cc -c gcc-head run" make -C . local --no-print-directory
