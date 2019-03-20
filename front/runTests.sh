#!/bin/bash
set -e
set -o pipefail

rm -f coverage_results.txt
nyc mocha --recursive -r ignore-styles -r ts-node/register  -r ./jsdom.js "src/**/*.spec.tsx" --extension spec.tsx | tee -a coverage_results.txt
nyc report --reporter=text-lcov > coverage.lcov

grep ^Statements coverage_results.txt | awk '{print $5}' | awk -F"/" 'BEGIN { max = -inf } { if ($1 > 0+max){ max = $1; c = $1; t = $2 } }  END { print "TOTAL     "t"     "(t - c)"     "(c/t) * 100"%" }'
rm -f coverage_results.txt
