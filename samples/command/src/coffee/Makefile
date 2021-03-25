#
# Makefile

COFFEESCRIPT=coffee

local:
	${COFFEESCRIPT} sample.coffee

wandbox:
	make -C . local --no-print-directory COFFEESCRIPT="wandbox-coffee run"
