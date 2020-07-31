#
# Makefile

CSHARP=

local:
	${CSHARP} sample.cs test.cs

wandbox:
	make -C . local --no-print-directory CSHARP="wandbox-cs run"
