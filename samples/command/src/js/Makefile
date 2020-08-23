#
# Makefile

JAVASCRIPT=node

local:
	# --experimental-modules
	${JAVASCRIPT} --experimental-modules sample.js

wandbox:
	make -C . local --no-print-directory JAVASCRIPT="wandbox-node run"
