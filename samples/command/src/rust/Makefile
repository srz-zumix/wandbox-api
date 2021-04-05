#
# Makefile

CARGO:=cargo
RUST:=rustc

local:
	${CARGO} run
	${CARGO} run --bin main2
	${CARGO} run --bin main3
	$(RUST) src/sample.rs

clean:
	rm -rf sample

wandbox:
	make -C . local --no-print-directory CARGO="wandbox-cargo" RUST="wandbox-rustc run"
