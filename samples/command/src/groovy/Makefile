#
# Makefile

GROOVY=groovy

local:
	${GROOVY} -cp . sample.groovy

wandbox:
	make -C . local --no-print-directory GROOVY="wandbox-groovy run"
