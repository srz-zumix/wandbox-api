#
# Makefile

PONYC:=ponyc
IGNORE_ERROR:=-

local:
	${PONYC} simple sample sample2
	${PONYC} sample sample2
	make -C simple ${MAKEGOALS}
	make -C sample ${MAKEGOALS}

clean:
	rm -f sample1 sample21
	
wandbox:
	${IGNORE_ERROR} make -C . local --no-print-directory PONYC="wandbox-ponyc run"
