#!/usr/bin/env bash

undo_rollout() {

  # Undo an Integrates rollout

  set -e

  if [[ "$1" == 'app' ]]; then
    kubectl rollout undo deploy/integrates-app
    return 0
  elif [[ "$1" == 'bot' ]]; then
    kubectl rollout undo deploy/integrates-bot
    return 0
  else
    echo 'Only app and bot params accepted'
  fi
  return 1
}

deploy_newrelic() {

  #Script to save a deployment record in New Relic
  #Reference: https://rpm.newrelic.com/api/explore/application_deployments/create

  set -e

  local NEW_RELIC_URL
  local COMMITTER_EMAIL
  local LAST_COMMITS_MASTER
  local CHANGELOG

  NEW_RELIC_URL='https://api.newrelic.com/v2/applications'
  COMMITTER_EMAIL=$(git log -1 --pretty=format:'%ce')

  if [ $SCHEDULE ]; then
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
        \"description\": \"$NEW_RELIC_ENVIRONMENT\",
        \"user\": \"$COMMITTER_EMAIL\"
      }
    }"
}

deploy_k8s() {

  # Deploys new Integrates version to production

  set -e

  # import functions
  . ci-scripts/helpers/others.sh

  # Logs in to vault in order to read vault vars
  vault_login

  local K8S_CONTEXT
  local B64_VAULT_HOST
  local B64_VAULT_TOKEN
  local CONFIG

  K8S_CONTEXT=$(kubectl config current-context)
  B64_VAULT_HOST=$(echo -n "$VAULT_HOST" | base64)
  B64_VAULT_TOKEN=$(echo -n "$VAULT_TOKEN" | base64)
  CONFIG='deploy/integrates-k8s.yaml'

  kubectl config set-context "$K8S_CONTEXT" --namespace serves

  if ! kubectl get secret gitlab-reg; then
    echo "Creating secret to access Gitlab Registry..."
    kubectl create secret docker-registry gitlab-reg \
      --docker-server="${CI_REGISTRY}" \
      --docker-username="${GITLAB_USER}" \
      --docker-password="${GITLAB_PASS}" \
      --docker-email="${GITLAB_EMAIL}"
  fi

  sed -i "s/\$VAULT_HOST/$B64_VAULT_HOST/g" "$CONFIG"
  sed -i "s/\$VAULT_TOKEN/$B64_VAULT_TOKEN/g" "$CONFIG"
  sed -i "s/\$DATE/$(date)/g" "$CONFIG"

  kubectl apply -f "$CONFIG"

  if ! kubectl rollout status deploy/integrates-app --timeout=8m; then
    undo_rollout app
    return 1
  fi

  if ! kubectl rollout status deploy/integrates-bot --timeout=5m; then
    undo_rollout bot
    return 1
  fi

  curl https://api.rollbar.com/api/1/deploy/ \
    -F access_token="$ROLLBAR_ACCESS_TOKEN" \
    -F environment="$FI_ROLLBAR_ENVIRONMENT" \
    -F revision="$CI_COMMIT_SHA" \
    -F local_username="$CI_COMMIT_REF_NAME"

  deploy_newrelic

  rm deploy/integrates-k8s.yaml
}

deploy_k8s
