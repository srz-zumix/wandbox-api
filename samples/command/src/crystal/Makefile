#
# Makefile

CRYSTAL:=crystal
IGNORE_ERROR:=-

local:
	${CRYSTAL} sample.cr

wandbox:
	${IGNORE_ERROR} make -C . local --no-print-directory CRYSTAL="wandbox-crystal run"
