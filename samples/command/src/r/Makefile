#
# Makefile

RSCRIPT=rscript

local:
	${RSCRIPT} sample.R

wandbox:
	make -C . local --no-print-directory RSCRIPT="wandbox-rscript run"
