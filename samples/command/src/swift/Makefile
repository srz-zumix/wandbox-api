#
# Makefile

SWIFT=swiftc
IGNORE_ERROR:=-

local:
	${SWIFT} main.swift test.swift

wandbox:
	${IGNORE_ERROR} make -C . local --no-print-directory SWIFT="wandbox-swift run"

clean:
	rm -rf main
