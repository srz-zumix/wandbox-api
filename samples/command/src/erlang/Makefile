#
# Makefile

EALANG:=erlc

local:
	${EALANG} prog.erl
	#erl -noshell -s sample main -s init stop

wandbox:
	make -C . local --no-print-directory EALANG="wandbox-erlang run"
