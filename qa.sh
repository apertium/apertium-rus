#!/bin/bash

# Takes the basename of the test scrpt in /test-scripts as an argument,
# an additional argument if the test script requires it, and runs the test.
#
# Usage: ./qa.sh (will default to './qa.sh rus')

if [ $# -eq 0 ]
then
    testToRun=rus.test
else
    testToRun=$1.test
fi

bash "test-scripts/$testToRun" "$2"
