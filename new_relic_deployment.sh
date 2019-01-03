#!/usr/bin/env bash

#Script to save a deployment record in New Relic
#Reference: https://rpm.newrelic.com/api/explore/application_deployments/create
COMMITTER_EMAIL=$(git log -1 --pretty=format:'%ce')
LAST_COMMITS_MASTER=$(git log "$CI_COMMIT_BEFORE_SHA"..HEAD --pretty=format:'%s')
CHANGELOG=$(printf "$LAST_COMMITS_MASTER" | sed -ze 's/\n/\\n/g' -e 's/\"/\\"/g')

curl -X POST 'https://api.newrelic.com/v2/applications/'"$NEW_RELIC_APP_ID"'/deployments.json' \
-H 'X-Api-Key:'"$NEW_RELIC_API_KEY" -i \
-H 'Content-Type:application/json' \
-d \
  '{
    "deployment": {
      "revision": "'"$CI_COMMIT_SHA"'",
      "changelog": "'"$CHANGELOG"'",
      "description": "'"$NEW_RELIC_ENVIRONMENT"'",
      "user": "'"$COMMITTER_EMAIL"'"
    }
  }'
