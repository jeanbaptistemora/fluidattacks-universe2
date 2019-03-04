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
