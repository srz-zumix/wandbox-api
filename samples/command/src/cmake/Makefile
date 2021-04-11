#
# Makefile

CMAKE_P=cmake -P

local:
	${CMAKE_P} sample.cmake

wandbox:
	make -C . local --no-print-directory CMAKE_P="wandbox-cmake run"
