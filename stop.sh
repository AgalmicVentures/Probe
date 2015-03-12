#!/bin/bash
PROCESSES=`ps xa | grep probe/__init__.py | grep -v grep`
if [[ $? -eq 1 ]]; then
	echo "Not running"
	exit
fi

PID=`echo $PROCESSES | awk '{print $1}'`
kill $PID
