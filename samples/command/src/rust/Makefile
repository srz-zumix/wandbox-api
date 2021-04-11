#
# Makefile

CARGO:=cargo
RUST:=rustc

local:
	$(CARGO) build --bins
	${CARGO} run
	${CARGO} -q r --bin main2
	${CARGO} -v r --bin main3
	$(RUST) src/sample.rs

test:
	$(CARGO) test
	$(CARGO) test --bin main
	$(CARGO) t --bin main2

clean:
	rm -rf sample

wandbox:
	make -C . local --no-print-directory CARGO="wandbox-cargo" RUST="wandbox-rustc run"
