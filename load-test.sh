#!/bin/bash

URL="http://<ip or url>"

declare -A answers

while true; do
    testresult=$(curl -s ${URL} )

    if [[ ${answers[$testresult]} == "" ]]; then
        answers[$testresult]=1
    else
        answers[$testresult]=$((${answers[$testresult]} + 1 ))
    fi
    clear
    for x in "${!answers[@]}"; do printf "[%s]=%s\n" "$x" "${answers[$x]}" ; done
    sleep 1
done