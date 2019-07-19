#!/usr/bin/env bash

danger() {

  # Runs danger on a Gitlab Merge Request

  local DANGER_GITLAB_API_TOKEN
  local DANGER_GITLAB_HOST
  local DANGER_GITLAB_API_BASE_URL
  local CI_MERGE_REQUEST_ID

  DANGER_GITLAB_API_TOKEN=$DANGER_TOKEN
  DANGER_GITLAB_HOST='gitlab.com'
  DANGER_GITLAB_API_BASE_URL='https://gitlab.com/api/v4'
  CI_MERGE_REQUEST_ID=$(
    git ls-remote -q origin merge-requests\*\head | \
    grep ${CI_COMMIT_SHA} | \
    sed 's/.*refs\/merge-requests\/\([0-9]*\)\/head/\1/g'
  )

  npm install --unsafe-perm
  bundle install
  bundle exec danger --verbose --fail-on-errors=true
}

danger
