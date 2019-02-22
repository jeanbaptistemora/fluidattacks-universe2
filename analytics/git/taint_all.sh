#!/usr/bin/env bash

# the /config.json contains a list of JSON with the path to the repository

output=$(cat /config.test.json \
  | jq -r ".[]|.location" \
    | sed -E 's/(\/git)\/(.*?)\/(.*)/\2 \1\/\2\/\3/g')

echo "$output" | while read line
do
  echo "$line"
  subs=$(echo "$line" | grep -o -E '^\w+')
  path=$(echo "$line" | grep -o -E ' .*$')
  ./analytics/git/taint.py set subscription $subs
  ./analytics/git/taint.py database push $path
done
