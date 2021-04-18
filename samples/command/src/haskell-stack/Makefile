#
# Makefile

STACK_RUN:=stack run
WANDBOX_CLI_OPTIONS:=--no-head
# WANDBOX_CLI_OPTIONS:=-c "ghc-8.4*"

local:
	${STACK_RUN}

wandbox:
	make -C . local --no-print-directory STACK_RUN="wandbox-stack ${WANDBOX_CLI_OPTIONS} run"
