#!/bin/sh

python3 /code/exploit-code.py > /tmp/fluidasserts.log
retval=$?
cat /tmp/fluidasserts.log

retval=0
grep -q "OPEN" /tmp/fluidasserts.log
if [[ x"$?" = x"0" ]]; then
    retval=1
fi

if [[ x"$retval" = x"1" ]]; then
    echo -e "\033[1;31mThere are open vulnerabilities!"
fi

exit $retval
