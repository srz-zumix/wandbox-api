#
# Makefile

SWIFT=swiftc

local:
	${SWIFT} main.swift test.swift

wandbox:
	make -C . local --no-print-directory SWIFT="wandbox-swift run"

clean:
	rm -rf main
