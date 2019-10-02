#!/usr/bin/env bash

run_danger() {

  # Run danger on a Gitlab Merge Request

  set -e

  export DANGER_GITLAB_API_TOKEN
  export CI_MERGE_REQUEST_ID

  DANGER_GITLAB_API_TOKEN="$DANGER_TOKEN"
  CI_MERGE_REQUEST_ID=$(
    git ls-remote -q origin merge-requests\*head | \
    grep "$CI_COMMIT_SHA" | \
    sed 's/.*refs\/merge-requests\/\([0-9]*\)\/head/\1/g'
  )

  npm install --unsafe-perm
  danger --verbose --fail-on-errors=true
}

run_danger
