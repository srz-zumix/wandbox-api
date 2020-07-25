#
# Makefile

PYTHON:=python

local:
	${PYTHON} sample.py ${TESTFILES}

wandbox:
	make -C . local --no-print-directory PYTHON="wandbox-python3 run"
	make -C . local --no-print-directory PYTHON="wandbox-python3 run" TESTFILES=test3.py
