#!/bin/bash

NODES=$(kubectl get nodes |grep cpod | awk '{print $1}')
while true;
do
    for NODE in ${NODES}
    do
        test=$(ping -c1 -w 1 $NODE)
        result=$(echo "$test" |grep loss | cut -d"," -f3)
        echo "$NODE - result :  $result"
    done
    sleep 1
    clear
done