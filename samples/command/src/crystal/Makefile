#
# Makefile

CRYSTAL:=crystal

local:
	${CRYSTAL} sample.cr

wandbox:
	make -C . local --no-print-directory CRYSTAL="wandbox-crystal run"
