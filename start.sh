#!/bin/bash

PROCESSES=`ps xa | grep Probe/__init__.py | grep -v grep`
if [[ $? -eq 0 ]]; then
	echo "Already running"
	exit
fi

echo "Starting..."
nohup python3 ./Probe/__init__.py &
sleep 1
echo "Started."

