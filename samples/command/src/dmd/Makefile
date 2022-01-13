#
# Makefile

DMD:=dmd

local:
	${DMD} sample.d test2.d packages/test.d

wandbox:
	make -C . local --no-print-directory DMD="wandbox-dmd run"
	# make -C . local --no-print-directory DMD="wandbox-gdmd run"
	make -C . local --no-print-directory DMD="wandbox-ldmd2 run"

clean:
	rm -rf *.o sample
