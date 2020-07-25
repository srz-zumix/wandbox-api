#
# Makefile

SUBDIRS := $(wildcard src/*/.)

all: $(SUBDIRS)

$(SUBDIRS):
	make -C $@ wandbox

.PHONY: all $(SUBDIRS)
