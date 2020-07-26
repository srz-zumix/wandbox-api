#
# Makefile

PYTHON:=python

local:
	${PYTHON} sample.py ${TESTFILES}

wandbox:
	make -C . local --no-print-directory PYTHON="wandbox-python3 run"
	make -C . local --no-print-directory PYTHON="wandbox-python3 run" TESTFILES=test3.py
	(cd .. && wandbox-python3 run python/sample.py)
	wandbox -l Python run sample.py test.py test2.py test3.py test4.py subdir/test5.py
