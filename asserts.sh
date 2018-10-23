#!/bin/sh

asserts --show-open /code/exploit-code.py > /tmp/fluidasserts.log
retval=0

if grep -q OPEN /tmp/fluidasserts.log
then
  cat /tmp/fluidasserts.log
  retval=1
fi

exit $retval
