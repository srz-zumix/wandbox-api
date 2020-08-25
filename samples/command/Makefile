#
# Makefile

SUBDIRS := $(wildcard src/*)
SUBDIRS_NAME = $(SUBDIRS:src/%=%)

all: $(SUBDIRS)

$(SUBDIRS_NAME) : % : src/%

$(SUBDIRS):
	make -C $@ wandbox

.PHONY: all $(SUBDIRS)
