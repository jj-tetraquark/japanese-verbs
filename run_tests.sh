#!/bin/sh
py=""
if [ ! -z "$(which python)" ]; then
    py="python"
else
    echo "Cannot find python, can't run tests!"
fi

if [ ! -z "$(which python3)" ]; then
    incompatible=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:3])))' | grep "3.0\|3.1\|3.2")
    if [ -z "$incompatible" ]; then
        py=python3
    else
        echo "Do not support python3 prior to 3.3. Running tests with python2"
    fi
fi

$py -m lib.tests
$py -m controllers.tests
