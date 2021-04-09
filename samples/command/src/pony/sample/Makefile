#
# Makefile

PONYC:=ponyc

local:
	${PONYC} .

clean:
	rm -f sample
	
wandbox:
	make -C . local --no-print-directory PONYC="wandbox-ponyc run"
