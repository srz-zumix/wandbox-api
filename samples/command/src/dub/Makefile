#
# Makefile

DUB:=dub

local:
	${DUB} run

wandbox:
	make -C . local --no-print-directory DUB="wandbox-dub"

clean:
	rm -rf .dub sample
