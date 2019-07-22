#!/usr/bin/env sh

undo_rollout() {
  if [ "$1" = 'app' ]; then
    kubectl rollout undo deploy/integrates
    exit 1
  elif ["$1" = 'bot' ]; then
    kubectl rollout undo deploy/integrates-bot
    exit 1
  else
    echo 'Only app and bot params accepted'
  fi
}

deploy_newrelic() {

  #Script to save a deployment record in New Relic
  #Reference: https://rpm.newrelic.com/api/explore/application_deployments/create

  local NEW_RELIC_URL
  local COMMITTER_EMAIL
  local LAST_COMMITS_MASTER
  local CHANGELOG

  NEW_RELIC_URL='https://api.newrelic.com/v2/applications'
  COMMITTER_EMAIL=$(git log -1 --pretty=format:'%ce')
  LAST_COMMITS_MASTER=$(
    git log "$CI_COMMIT_BEFORE_SHA"..HEAD --pretty=format:'%s'
  )
  CHANGELOG=$(
    printf "$LAST_COMMITS_MASTER" | sed -ze 's/\n/\\n/g' -e 's/\"/\\"/g'
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

  local K8S_CONTEXT
  local B64_VAULT_HOST
  local B64_VAULT_TOKEN

  K8S_CONTEXT=$(kubectl config current-context)
  B64_VAULT_HOST=$(echo -n $VAULT_HOST | base64)
  B64_VAULT_TOKEN=$(echo -n $VAULT_TOKEN | base64)

  kubectl config set-context "$K8S_CONTEXT" --namespace serves

  if ! kubectl get secret gitlab-reg; then
    echo "Creating secret to access Gitlab Registry..."
    kubectl create secret docker-registry gitlab-reg \
      --docker-server="${CI_REGISTRY}" \
      --docker-username="${GITLAB_USER}" \
      --docker-password="${GITLAB_PASS}" \
      --docker-email="${GITLAB_EMAIL}"
  fi

  sed -i 's/$VAULT_HOST/'"$B64_VAULT_HOST"'/;
    s/$VAULT_TOKEN/'"$B64_VAULT_TOKEN"'/;
    s/$DATE/'"$(date)"'/g'
    integrates-k8s.yaml

  kubectl apply -f integrates-k8s.yaml

  kubectl rollout status deploy/integrates --timeout=5m || undo_rollout app
  kubectl rollout status deploy/integrates-bot --timeout=5m || undo_rollout bot

  curl https://api.rollbar.com/api/1/deploy/
    -F access_token=$ROLLBAR_ACCESS_TOKEN
    -F environment=$FI_ROLLBAR_ENVIRONMENT
    -F revision=$CI_COMMIT_SHA
    -F local_username="$CI_COMMIT_REF_NAME"

  deploy_newrelic
}

deploy_k8s
