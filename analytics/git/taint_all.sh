#!/usr/bin/env bash

# continuous repo
continuous_path="/git/fluidsignal/continuous"

# /config.json: A list of JSON with subscription, repository, location and branches
output=$(cat /config.json \
  | jq -r ".[]|.location" \
    | sed -E 's/(\/git)\/(.*?)\/(.*)/\2 \1\/\2\/\3/g')

./analytics/git/taint.py set username "lines.csv"
echo "$output" | while read line
do
  subs=$(echo "$line" | grep -o -E '^[a-zA-Z0-9_-]+')
  path=$(echo "$line" | grep -o -E ' .*$')
  echo "subscription: $subs"
  echo "path: $path"

  ./analytics/git/taint.py set subscription $subs
  ./analytics/git/taint.py database push $path
  lines_csv_path="$continuous_path/subscriptions/${subs/-//}/lines.csv"
  if [ -f "$lines_csv_path" ]; then
    ./analytics/git/taint.py database wring "$lines_csv_path"
  fi
  echo ""
done
