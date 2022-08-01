#
# Makefile

SCALA=scalac
IGNORE_ERROR:=-

local:
	${SCALA} simple/simple.scala
	${SCALA} *.scala test1/*.scala

# test:
# 	${SCALA} sample.scala "test3.scala" "test4.scala" "test1/test1.scala" "test1/test2.scala"

clean:
	rm -f **/*.class *.class

wandbox:
	${IGNORE_ERROR} make -C . local --no-print-directory SCALA="wandbox-scalac run"
