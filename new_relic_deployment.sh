#!/usr/bin/env bash

#Script to save a deployment record in New Relic
#Reference: https://rpm.newrelic.com/api/explore/application_deployments/create

curl -X POST 'https://api.newrelic.com/v2/applications/'"$NEW_RELIC_APP_ID"'/deployments.json' \
-H 'X-Api-Key:'"$NEW_RELIC_API_KEY" -i \
-H 'Content-Type:application/json' \
-d \
  '{
    "deployment": {
      "revision": "'"$CI_COMMIT_SHA"'",
      "changelog": "'"$CI_COMMIT_MESSAGE"'"
      "description": "'"$NEW_RELIC_ENVIRONMENT"'",
      "user": "'"$CI_COMMIT_REF_NAME"'"
    }
  }'
