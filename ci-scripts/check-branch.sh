#!/usr/bin/env bash

git fetch --prune &> /dev/null
LAST_MASTER_COMMIT=$(git show-ref --heads -s "master")
LAST_COMMON_COMMIT=$(git merge-base "master" "origin/$CI_COMMIT_REF_NAME")
if [ "$LAST_COMMON_COMMIT" != "$LAST_MASTER_COMMIT" ]; then
  echo "Make sure to rebase your branch before posting a MR."
  exit 1
else
  echo "Branch rebase check OK..."
fi
