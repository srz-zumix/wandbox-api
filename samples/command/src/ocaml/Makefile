#
# Makefile

OCAMLOPT:=ocamlopt
# NOTE: head version is not stable
# WANDBOX_CLI_OPTIONS:=--no-head
IGNORE_ERROR:=-

local:
	${OCAMLOPT} sample.ml

wandbox:
	${IGNORE_ERROR} make -C . local --no-print-directory OCAMLOPT="wandbox-ocamlopt --no-ocaml-core ${WANDBOX_CLI_OPTIONS} run"
