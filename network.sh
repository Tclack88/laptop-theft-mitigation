#!/bin/bash
NOW=$(date +"%d%b%Y-%T")
sudo iwlist scan | grep ESSID &> /dev/null
nmcli -f SSID,BSSID,DEVICE dev wifi > tmp/NW-$NOW.txt 
