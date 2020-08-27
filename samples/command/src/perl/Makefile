#
# Makefile

PERL:=perl

local:
	${PERL} sample.pl

wandbox:
	make -C . local --no-print-directory PERL="wandbox-perl run"
