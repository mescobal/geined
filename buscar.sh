#!/bin/bash
clear
echo '-------------------------------------'
grep -A 0 -n -i --colour=auto $1 *.*
echo '-------------------------------------'
grep -A 0 -n -i --colour=auto $1 css/*.*
grep -A 0 -n -i --colour=auto $1 js/*.*


