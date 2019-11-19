#!/bin/bash

STATUS=0

printf "[+] Test: run all src under tests/ .\n"

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
        STATUS=1
    fi

    if [ -e $f.input ]; then
        cpuex_sim debug.output.o -i $f.input -o debug.uart.output > debug.output.exec
    else
        cpuex_sim debug.output.o -o debug.uart.output > debug.output.exec
    fi
    
    diff -b debug.output.exec $f.exec.expected > /dev/null
    ret=$?
    if [ $ret -eq 0 ] ;then
        printf "\e[32m$f: exec passed.\e[m\n"
    else 
        printf "\e[31m$f: exec failed.\e[m\n"
        diff $f.exec.expected debug.output.exec
        STATUS=1
    fi

    if [ -e $f.uart.expected ] ;then
       diff -b debug.uart.output $f.uart.expected > /dev/null
       ret=$?
       if [ $ret -eq 0 ] ;then
           printf "\e[32m$f: uart passed.\e[m\n"
       else 
           printf "\e[31m$f: uart failed.\e[m\n"
           diff $f.uart.expected debug.output.uart
           STATUS=1
       fi
    fi       
done

rm -rf debug.*

if [ $STATUS -eq 0 ];  then
    printf "\e[32m[+] Yay! testing passed.\e[m\n"    
else
    printf "\e[31m[-] Oops, testing failed.\e[m\n"
fi

exit $STATUS
