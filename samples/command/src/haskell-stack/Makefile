#
# Makefile

STACK_RUN:=stack run
# NOTE: head version is not work
WANDBOX_CLI_OPTIONS:=--no-head

local:
	${STACK_RUN}

wandbox:
	make -C . local --no-print-directory STACK_RUN="wandbox-stack ${WANDBOX_CLI_OPTIONS} run"
