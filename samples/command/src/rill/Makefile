#
# Makefile

RILL:=rillc

local:
	${RILL} sample.rill test1.rill

wandbox:
	make -C . local --no-print-directory RILL="wandbox-rillc run"

