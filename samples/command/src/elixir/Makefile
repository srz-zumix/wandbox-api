#
# Makefile

ELIXIR:=elixir
MIX:=mix

local:
	${ELIXIR} sample.exs
	(cd sample && ${MIX} test) 

wandbox:
	make -C . local --no-print-directory ELIXIR="wandbox-elixir run" MIX="wandbox-mix run"
