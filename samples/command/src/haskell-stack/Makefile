#
# Makefile

STACK_RUN:=stack run
WANDBOX_CLI_OPTIONS:=--no-head
# WANDBOX_CLI_OPTIONS:=-c "ghc-8.4*"
IGNORE_ERROR:=-

local:
	${STACK_RUN}

wandbox:
	# prog.exe: failed to create OS thread: Cannot allocate memory
	${IGNORE_ERROR} make -C . local --no-print-directory STACK_RUN="wandbox-stack ${WANDBOX_CLI_OPTIONS} run"
