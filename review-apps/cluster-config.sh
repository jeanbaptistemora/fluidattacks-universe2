#!/usr/bin/env bash
# This scripts manages the deployment of the Review Apps,
# which allow to view a live site through a public IP with the
# changes introduced by the developer, before accepting changes into
# production.


function echo-blue() {
  echo -e '\033[1;34m'"${1}"'\033[0m'
}

function find_resource() {
  local resource="${1}"
  local regex="${2}"
  shift 2
  local options="$@"
  if [ -z "${options}" ]; then
    kubectl get "${resource}" | egrep "${regex}"
  else
    kubectl get "${resource}" | egrep "${regex}" "${options}"
  fi
}

function replace_env_variables() {
  local files=( "$@" )
  for file in "${files[@]}"; do
    envsubst < "${file}" > tmp
    mv tmp "${file}"
  done
}

export ENV_NAME

ENV_NAME='development'

# Import functions
. ci-scripts/helpers/sops.sh

aws_login "$ENV_NAME"

# Set namespace preference for kubectl commands
echo-blue "Setting namespace preferences..."
kubectl config set-context \
  "$(kubectl config current-context)" --namespace="$CI_PROJECT_NAME"

# Check secret to pass env variables to container
export DATE="$(date)"
export B64_AWS_ACCESS_KEY_ID="$(echo -n $AWS_ACCESS_KEY_ID | base64)"
export B64_AWS_SECRET_ACCESS_KEY="$(echo -n $AWS_SECRET_ACCESS_KEY | base64)"
export B64_JWT_TOKEN="$(echo -n $JWT_TOKEN | base64)"
replace_env_variables \
  review-apps/variables.yaml \
  review-apps/ingress.yaml \
  review-apps/deploy-integrates.yaml
kubectl apply -f review-apps/variables.yaml
kubectl apply -f review-apps/ingress.yaml

# Deploy pod and service
echo "Deploying latest image..."
kubectl apply -f review-apps/deploy-integrates.yaml
kubectl rollout status "deploy/review-${CI_COMMIT_REF_SLUG}" --timeout=5m ||
  { echo-blue "Review environment failed to deploy" && exit 1; }

# Erase file with keys
rm review-apps/variables.yaml
