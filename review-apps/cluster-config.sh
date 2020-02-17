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

function issue_domain_certificate() {
  local manifest="${1}"
  local issuer="${2}"
  local certificate="${3}"
  kubectl delete issuer "${issuer}" ||
    echo "No previous Let's Encrypt account found."
  kubectl delete certificate "${certificate}" ||
    echo "No previous certificate found."
  export RA_ACCESS_KEY="$AWS_ACCESS_KEY_ID"
  export RA_SECRET_KEY="$AWS_SECRET_ACCESS_KEY"
  rm review.json
  sleep 15
  echo "Creating secret with AWS credentials..."
  kubectl create secret generic ra-aws --type=opaque \
    --from-literal=sec-key="$RA_SECRET_KEY"
  echo "Creating Issuer and Certificate to enable communication through HTTPS..."
  replace_env_variables "${manifest}"
  kubectl apply -f "${manifest}"
  while ! kubectl describe certificate "${certificate}" | grep 'CertIssued'; do
    echo-blue "Issuing certificate..."
    sleep 10
  done
  kubectl delete secret ra-aws
}

function validate_domain_certificate() {
  local manifest="${1}"
  local issuer="$(cat ${manifest} | grep -m1 -Po '(?<=name: ).*')"
  local certificate="$(cat ${manifest} | sed -n -e '/Certificate/,$p' | \
                      grep -m1 -Po '(?<=name: ).*')"
  local secret="$(cat ${manifest} | grep -Po '(?<=secretName: ).*')"
  if find_resource secret "${secret}"; then
    local secret_age="$(kubectl get secret ${secret} | \
                      grep -Po '(?<=\s)[0-9]+d' | sed 's/.$//')"
    if [ -z "${secret_age}" ]; then
      echo-blue "Domain certificate is valid."
    elif [ "${secret_age}" -gt 80 ]; then
      kubectl delete secret "${secret}"
      issue_domain_certificate "${manifest}" "${issuer}" "${certificate}"
    fi
  else
    issue_domain_certificate "${manifest}" "${issuer}" "${certificate}"
  fi
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

# Check resources to enable TLS communication
validate_domain_certificate review-apps/tls.yaml

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
