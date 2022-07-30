#!/bin/bash
# This file is a "Hello, world!" in Bash script for wandbox.
echo Hello, Wandbox!

source test1.sh
. test2-1.sh
. ./test2-2.sh;

# ./test3.sh
echo ${SHELL}
${SHELL} ./test3.sh
sh ./test3.sh
bash ./test3.sh

# if [ "$1" = "wandbox" ]; then
#   ls /opt/wandbox
# fi

. "test 4;.sh";
source "test 4.sh"; . ./test4.sh;source "./test 4;;.sh"

echo $*

if [ "$1" != "local" ]; then
    if [ "$1" != "wandbox" ]; then
        exit 1
    fi
fi


# Bash script references:
#   https://www.gnu.org/software/bash/manual/bashref.html
#   http://shellscript.sunone.me ( Japanese )
