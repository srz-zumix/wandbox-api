#
# Makefile

ZIG:=zig

local:
	${ZIG} run main.zig

wandbox:
	make -C . local --no-print-directory ZIG="wandbox-zig"

clean:
	rm -rf main
