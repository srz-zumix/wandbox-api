#
# Makefile

OPENSSL:=openssl


local: test.key.pub

test.key:
	${OPENSSL} genrsa -out test.key 2048

test.key.pub: test.key
	${OPENSSL} rsa -in test.key -pubout -out test.key.pub

clean:
	rm -rf test.key
	rm -rf test.key.pub

wandbox:
	make -C . local --no-print-directory OPENSSL="wandbox-ssl --no-head"
