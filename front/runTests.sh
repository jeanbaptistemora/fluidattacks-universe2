#!/bin/sh

testFiles=$(find src/ -name '*.spec.tsx')
exitCode=0

for test in $testFiles
do
  mocha -r ignore-styles -r ts-node/register -r ./jsdom.js "$test";
  exitCode=$?

  if [ "$exitCode" -ne 0 ]
  then
    break
  fi
done

exit $exitCode
