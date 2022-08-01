#
# Makefile

VIM=vim
IGNORE_ERROR:=-

local:
	${VIM} -X -N -u NONE -i NONE -V1 -e -s -S sample.vim +qall!

wandbox:
	${IGNORE_ERROR} make -C . local --no-print-directory VIM="wandbox-vim -s run"
