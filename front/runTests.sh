#!/bin/sh

testFiles=$(find src/ -name '*.spec.tsx')
exitCode=0

rm -f coverage_results.txt
for test in $testFiles
do
  nyc mocha -r ignore-styles -r ts-node/register -r ./jsdom.js "$test" | tee -a coverage_results.txt
  exitCode=$?

  if [ "$exitCode" -ne 0 ]
  then
    break
  fi
done

grep ^Statements coverage_results.txt | awk '{print $5}' | awk -F"/" 'BEGIN { max = -inf } { if ($1 > 0+max){ max = $1; c = $1; t = $2 } }  END { print "TOTAL     "t"     "(t - c)"     "(c/t) * 100"%" }'
rm -f coverage_results.txt
exit $exitCode
