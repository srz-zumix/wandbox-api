#
# Makefile

LAZYK:=lazyk
IGNORE_ERROR:=-

local:
	${LAZYK} sample.lazy

wandbox:
	${IGNORE_ERROR} make -C . local --no-print-directory LAZYK="wandbox-lazyk run"
