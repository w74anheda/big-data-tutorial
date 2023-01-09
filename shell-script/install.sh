#!/bin/bash

a=0
while [ "$a" -lt 30 ]
do
    echo $a
    a=`expr $a + 1`

    if [ "$a" -eq 20 ]
        then
            echo '****'
        else
            echo '+++++++++'
        fi

    if [ "$a" -gt 15 ]
        then
            echo '----'
        fi
done