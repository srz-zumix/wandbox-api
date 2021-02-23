#
# Makefile

GHC:=ghc
# WANDBOX_CLI_OPTIONS:=--no-head

local:
	${GHC} sample.hs

wandbox:
	make -C . local --no-print-directory GHC="wandbox-ghc ${WANDBOX_CLI_OPTIONS} run"
