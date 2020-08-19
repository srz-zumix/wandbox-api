#
# Makefile

GOBUILD=go build

local:
	${GOBUILD} sample.go

wandbox:
	make -C . local --no-print-directory GOBUILD="wandbox-go --gcflags-m run"
