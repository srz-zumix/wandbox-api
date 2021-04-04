#
# Makefile

SQLITE:=sqlite3

local:
	cat sample.sql | ${SQLITE}

wandbox:
	make -C . local --no-print-directory SQLITE="wandbox-sqlite3 run"
