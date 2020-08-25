#
# Makefile

TYPESCRIPT=tsc

local:
	${TYPESCRIPT} --module es2015 sample.ts

wandbox:
	make -C . local --no-print-directory TYPESCRIPT="wandbox-tsc run"
	# make -C . local --no-print-directory TYPESCRIPT="wandbox-tsc -r=--experimental-modules run"
