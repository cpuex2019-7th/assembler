#!/bin/bash

for f in `ls tests/*.S`; do
    cpuex_asm debug.output.o $f    
    cpuex_disasm debug.output.o | awk -F';' '{print $1}' > debug.output.disasm    
    diff -b debug.output.disasm $f.disasm.expected > /dev/null
    ret=$?
    if [ $ret -eq 0 ] ;then
        printf "\e[32m$f: disasm passed.\e[m\n"
    else 
        printf "\e[31m$f: disasm failed.\e[m\n"
        diff $f.disasm.expected debug.output.disasm
    fi

    cpuex_sim debug.output.o > debug.output.exec
    diff -b debug.output.exec $f.exec.expected > /dev/null
    ret=$?
    if [ $ret -eq 0 ] ;then
        printf "\e[32m$f: exec passed.\e[m\n"
    else 
        printf "\e[31m$f: exec failed.\e[m\n"
        diff $f.exec.expected debug.output.exec
    fi
done

rm -rf debug.*
