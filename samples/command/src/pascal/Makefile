#
# Makefile

PASCAL:=fpc

local:
	${PASCAL} sample.pas

wandbox:
	make -C . local --no-print-directory PASCAL="wandbox-fpc run"
