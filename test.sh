#!/bin/bash

for f in `ls tests/*.S`; do
    cpuex_asm debug.output.o $f
    cpuex_disasm debug.output.o | awk -F';' '{print $1}' > debug.output.txt
    diff debug.output.txt $f.expected
    ret=$?
    if [ $ret -eq 0 ] ;then
        printf "\e[32m$f: passed.\e[m\n"
    else 
        printf "\e[31m$f: failed.\e[m\n"
        echo "expected: "
        cat $f.expected
        echo "got: "
        cat debug.output.txt
    fi
done

rm -rf debug.*
