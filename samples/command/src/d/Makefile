#
# Makefile

DMD:=dmd

local:
	${DMD} sample.d test2.d packages/test.d

wandbox:
	make -C . local --no-print-directory DMD="wandbox-dmd run"
	# collect2: fatal error: ld terminated with signal 25 [File size limit exceeded], core dumped
	# compilation terminated.
	# make -C . local --no-print-directory DMD="wandbox-gdc run"
	make -C . local --no-print-directory DMD="wandbox-ldc run"

clean:
	rm -rf *.o sample
