#
# Makefile

OPENSSL:=openssl

local:
	${OPENSSL} genrsa 2048

wandbox:
	make -C . local --no-print-directory OPENSSL="wandbox-ssl"
