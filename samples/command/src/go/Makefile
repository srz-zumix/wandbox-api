#
# Makefile

GOBUILD=go build
# NOTE: head version is not stable
WANDBOX_CLI_OPTIONS:=--no-head

local:
	${GOBUILD} sample.go

wandbox:
	make -C . local --no-print-directory GOBUILD="wandbox-go ${WANDBOX_CLI_OPTIONS} run"
	# make -C . local --no-print-directory GOBUILD="wandbox-go ${WANDBOX_CLI_OPTIONS} --gcflags-m run"
