#
# Makefile

GHC:=ghc
# NOTE: head version is not work
WANDBOX_CLI_OPTIONS:=--no-head

local:
	${GHC} sample.hs

wandbox:
	make -C . local --no-print-directory GHC="wandbox-ghc ${WANDBOX_CLI_OPTIONS} run"
