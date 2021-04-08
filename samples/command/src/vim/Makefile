#
# Makefile

VIM=vim

local:
	${VIM} -X -N -u NONE -i NONE -V1 -e -s -S sample.vim +qall!

wandbox:
	make -C . local --no-print-directory VIM="wandbox-vim run"
