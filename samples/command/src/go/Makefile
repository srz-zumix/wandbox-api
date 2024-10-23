#
# Makefile

GOBUILD=GO111MODULE=off go run
# NOTE: head version is not stable
WANDBOX_CLI_OPTIONS:=-c=go-1.16.3

local:
	${GOBUILD} sample.go

wandbox:
	make -C . local --no-print-directory GOBUILD="wandbox-go ${WANDBOX_CLI_OPTIONS} run"
	# make -C . local --no-print-directory GOBUILD="wandbox-go ${WANDBOX_CLI_OPTIONS} --gcflags-m run"
