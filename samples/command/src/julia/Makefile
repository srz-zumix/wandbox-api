#
# Makefile

JULIA:=julia

local:
	${JULIA} sample.jl

wandbox:
	make -C . local --no-print-directory JULIA="wandbox-julia run"
