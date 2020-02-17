#!/usr/bin/env bash

undo_rollout() {

  # Undo an Integrates rollout

  set -Eeuo pipefail
  kubectl rollout undo deploy/integrates-app
}

deploy_newrelic() {

  # Script to save a deployment record in New Relic
  # Reference: https://rpm.newrelic.com/api/explore/application_deployments/create

  set -Eeuo pipefail

  local ENV_NAME
  local NEW_RELIC_URL
  local COMMITTER_EMAIL
  local LAST_COMMITS_MASTER
  local CHANGELOG

  ENV_NAME='production'
  NEW_RELIC_URL='https://api.newrelic.com/v2/applications'
  COMMITTER_EMAIL=$(git log -1 --pretty=format:'%ce')

  if [ "$SCHEDULE" = '0' ]; then
    LAST_COMMITS_MASTER=$(
      git log HEAD~1..HEAD --pretty=format:'%s'
    )
  else
    LAST_COMMITS_MASTER=$(
      git log "$CI_COMMIT_BEFORE_SHA"..HEAD --pretty=format:'%s'
    )
  fi

  CHANGELOG=$(
    echo "$LAST_COMMITS_MASTER" | sed -ze 's/\n/\\n/g' -e 's/\"/\\"/g'
  )

  curl -X POST "$NEW_RELIC_URL/$NEW_RELIC_APP_ID/deployments.json" \
  -H 'X-Api-Key:'"$NEW_RELIC_API_KEY" -i \
  -H 'Content-Type:application/json' \
  -d \
    "{
      \"deployment\": {
        \"revision\": \"$CI_COMMIT_SHA\",
        \"changelog\": \"$CHANGELOG\",
        \"description\": \"$ENV_NAME\",
        \"user\": \"$COMMITTER_EMAIL\"
      }
    }"
}

deploy_k8s() {

  # Deploy new Integrates version to production

  if [ -z "$SCHEDULE" ]; then
    export SCHEDULE="1"
  fi

  set -Eeuo pipefail

  # Import functions
  . <(curl -s https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/sops.sh)
  . ci-scripts/helpers/sops.sh

  local ENV_NAME
  local K8S_CONTEXT
  local B64_AWS_ACCESS_KEY_ID
  local B64_AWS_SECRET_ACCESS_KEY
  local B64_JWT_TOKEN
  local CONFIG

  ENV_NAME='production'

  aws_login "$ENV_NAME"

  sops_env "secrets-$ENV_NAME.yaml" default \
    ROLLBAR_ACCESS_TOKEN \
    NEW_RELIC_API_KEY \
    NEW_RELIC_APP_ID

  K8S_CONTEXT="$(kubectl config current-context)"
  B64_AWS_ACCESS_KEY_ID="$(echo -n $AWS_ACCESS_KEY_ID | base64)"
  B64_AWS_SECRET_ACCESS_KEY="$(echo -n $AWS_SECRET_ACCESS_KEY | base64)"
  B64_JWT_TOKEN="$(echo -n $JWT_TOKEN | base64)"

  CONFIG='deploy/integrates-k8s.yaml'

  kubectl config set-context "$K8S_CONTEXT" --namespace serves

  sed -i "s/\$B64_AWS_ACCESS_KEY_ID/$B64_AWS_ACCESS_KEY_ID/g" "$CONFIG"
  sed -i "s/\$B64_AWS_SECRET_ACCESS_KEY/$B64_AWS_SECRET_ACCESS_KEY/g" "$CONFIG"
  sed -i "s/\$B64_JWT_TOKEN/$B64_JWT_TOKEN/g" "$CONFIG"
  sed -i "s/\$DATE/$(date)/g" "$CONFIG"

  kubectl apply -f "$CONFIG"

  if ! kubectl rollout status deploy/integrates-app --timeout=8m; then
    undo_rollout
    return 1
  fi

  curl https://api.rollbar.com/api/1/deploy/ \
    -F access_token="$ROLLBAR_ACCESS_TOKEN" \
    -F environment="$ENV_NAME" \
    -F revision="$CI_COMMIT_SHA" \
    -F local_username="$CI_COMMIT_REF_NAME"

  deploy_newrelic

  rm deploy/integrates-k8s.yaml
}

deploy_k8s
