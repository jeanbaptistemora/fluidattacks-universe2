#!/usr/bin/env bash

# continuous repo
continuous_path="/git/fluidattacks/continuous"

# /config.json: A list of JSON with subscription, repository, location and branches
output=$(cat /config.json \
  | jq -r ".[]|.location" \
    | sed -E 's/(\/git)\/(.*?)\/(.*)/\2 \1\/\2\/\3/g')

# push every repo to the database
echo "$output" | while read line
do
  subs=$(echo "$line" | grep -o -E '^[a-zA-Z0-9_-]+')
  subs=${subs#*-}
  path=$(echo "$line" | grep -o -E ' .*$')
  echo "subscription: $subs"
  echo "path: $path"
  ./analytics/git/taint.py set subscription $subs
  ./analytics/git/taint.py database push $path
  echo ""
done

# extract information about clean lines from every lines.csv
./analytics/git/taint.py set username "lines.csv"
echo "$output" | grep -o -E '^[a-zA-Z0-9_-]+' | uniq | while read subs
do
  lines_csv_path="$continuous_path/subscriptions/${subs/-//}/toe/lines.csv"
  echo "path: $lines_csv_path"
  if [ -f "$lines_csv_path" ]; then
    ./analytics/git/taint.py database wring "$lines_csv_path"
  fi
  echo ""
done
