#
# Makefile

JAVAC:=javac

local:
	${JAVAC} sample.java test.java

wandbox:
	make -C . local --no-print-directory JAVAC="wandbox-java run"

clean:
	rm -rf *.class
