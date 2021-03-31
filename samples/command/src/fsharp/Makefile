#
# Makefile

FSHARP=fsharpc

local:
	${FSHARP} test1.fs sample.fs
	# mono sample.exe

wandbox:
	make -C . local --no-print-directory FSHARP="wandbox-fsharpc run"
