#
# Makefile

PONYC:=ponyc

local:
	${PONYC}

clean:
	rm -f simple
	
wandbox:
	make -C . local --no-print-directory PONYC="wandbox-ponyc run"
