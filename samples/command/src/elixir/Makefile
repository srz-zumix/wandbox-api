#
# Makefile

ELIXIR:=elixir
MIX:=mix
IGNORE_ERROR:=-

local:
	${ELIXIR} sample.exs
	(cd sample && ${MIX} test) 

wandbox:
	${IGNORE_ERROR} make -C . local --no-print-directory ELIXIR="wandbox-elixir run" MIX="wandbox-mix run"
