#
# Makefile

WSHELL:=${SHELL}
OPTION:=${MAKECMDGOALS}

local:
	${WSHELL} sample.sh ${OPTION}

wandbox:
	make -C . local --no-print-directory OPTION=${OPTION} WSHELL="wandbox-bash"
