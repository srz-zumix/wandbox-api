#
# Makefile

ELIXIR:=elixir

local:
	${ELIXIR} sample.exs

wandbox:
	make -C . local --no-print-directory ELIXIR="wandbox-elixir run"
