#
# Makefile

EALANG:=erlc
IGNORE_ERROR:=-

local:
	${EALANG} prog.erl
	#erl -noshell -s sample main -s init stop

wandbox:
	${IGNORE_ERROR} make -C . local --no-print-directory EALANG="wandbox-erlc run"
