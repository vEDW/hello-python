#!/bin/bash

URL="http://<ip or url>"

declare -A answers

get_result() {
        #returns json
        RESPONSE=$(curl -s -w '####%{response_code}' ${URL})
        HTTPSTATUS=$(echo ${RESPONSE} |awk -F '####' '{print $2}')
        case $HTTPSTATUS in

                200)    
                        echo ${RESPONSE} |awk -F '####' '{print $1}'
                        ;;

                503)    
                        echo "Not Ready"
                        ;;
                *)      
                         echo ${RESPONSE} |awk -F '####' '{print $1}'
                        ;;

        esac
}


while true; do
    testresult=$(get_result)

    if [[ ${answers[$testresult]} == "" ]]; then
        answers[$testresult]=1
    else
        answers[$testresult]=$((${answers[$testresult]} + 1 ))
    fi
    clear
    for x in "${!answers[@]}"; do printf "[%s]=%s\n" "$x" "${answers[$x]}" ; done
    sleep 1
done