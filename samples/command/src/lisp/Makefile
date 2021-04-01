#
# Makefile

SBCL:=sbcl

local:
	${SBCL} sample.lisp

wandbox:
	make -C . local --no-print-directory SBCL="wandbox-sbcl run"
