#!/bin/bash

# shellcheck disable=SC2086

EXIT_FAIL=0

git fetch --prune &> /dev/null
N_COMMITS=$(git log --oneline origin/master..origin/$CI_COMMIT_REF_NAME | wc -l)
for ((i = 0 ; i < N_COMMITS ; i++)); do
  if ! git rev-parse HEAD~$i | xargs git log -1 --pretty=%B | npx commitlint
  then
    EXIT_FAIL=1
  fi
done

DELTAS=$(git log --stat . | egrep "files? changed" | head -n 1 | cut -d, -f 2- | sed -e 's/[^0-9]/ /g' -e 's/^ *//g' -e 's/ *$//g' | tr -s ' ' | sed 's/ /\n/g' | { c=0; while read x; do c=$(($c+$x)); done; echo $c; })

echo "Commit has $DELTAS deltas."

if [[ $DELTAS -gt 200 ]]; then
  EXIT_FAIL=1
fi

if [[ x"$EXIT_FAIL" = x"1" ]]; then
    exit 1
fi
