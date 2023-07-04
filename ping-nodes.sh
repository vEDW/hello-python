#!/bin/bash

NODESELECTOR=v7mic
DOMAIN=cpod-v7mic-vlans.az-lhr.cloud-garage.net

NODES=$(kubectl get nodes |grep "${NODESELECTOR}" | awk '{print $1}')
while true;
do
    for NODE in ${NODES}
    do
        test=$(ping -c1 -w 1 $NODE.${DOMAIN})
        result=$(echo "$test" |grep loss | cut -d"," -f3)
        echo "$NODE - result :  $result"
    done
    sleep 1
    clear
done