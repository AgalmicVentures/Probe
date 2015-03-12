#!/bin/bash

PROCESSES=`ps xa | grep probe/__init__.py | grep -v grep`
if [[ $? -eq 0 ]]; then
	echo "Already running"
	exit
fi

echo "Starting..."
nohup ./probe/__init__.py &
sleep 1
echo "Started."

