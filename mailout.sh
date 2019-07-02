#!/bin/bash
echo | mailx -s "stolen laptop" $(for f in $(ls tmp/); do echo -n " -A tmp/$f "; done) myemail@something.com && rm tmp/*

