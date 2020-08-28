#
# Makefile

NIM:=nim c -r

local:
	${NIM} sample.nim

clean:
	rm -rf sample

wandbox:
	make -C . local --no-print-directory NIM="wandbox-nim run"
