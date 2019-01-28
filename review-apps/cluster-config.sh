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
  echo-blue "Generating dynamic AWS credentials..."
  vault read -format=json aws/creds/integrates-review > review.json
  export RA_ACCESS_KEY="$(cat review.json | jq -r '.data.access_key')"
  export RA_SECRET_KEY="$(cat review.json | jq -r '.data.secret_key')"
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
                       grep -Po '[0-9]+(d|h|m|s)$' | sed 's/.$//')"
    if [ "${secret_age}" -gt 85 ]; then
       issue_domain_certificate "${manifest}" "${issuer}" "${certificate}"
    else
      echo-blue "Domain certificate is valid."
    fi
  else
    issue_domain_certificate "${manifest}" "${issuer}" "${certificate}"
  fi
}

cd review-apps/

# Set namespace preference for kubectl commands
echo-blue "Setting namespace preferences..."
kubectl config set-context \
  "$(kubectl config current-context)" --namespace="$CI_PROJECT_NAME"

# Prepare manifests by replacing the value of Environmental Variables
replace_env_variables ingress.yaml
replace_env_variables deploy-integrates.yaml

# Check resources to enable TLS communication
validate_domain_certificate tls.yaml

# Check secret to pull images from Gitlab Registry and set if not present
if find_resource secret gitlab-reg; then
  echo-blue "Access to Gitlab Registry already configured."
else
  echo-blue "Creating secret to access Gitlab Registry..."
  kubectl create secret docker-registry gitlab-reg \
    --docker-server="$CI_REGISTRY" \
    --docker-username="$DOCKER_USER" --docker-password="$DOCKER_PASS" \
    --docker-email="$DOCKER_EMAIL"
fi

# Check secret to pass env variables to container
export VAULT_HOST_B64="$(echo -n ${VAULT_HOST} | base64)"
export VAULT_TOKEN_B64="$(echo -n ${VAULT_TOKEN} | base64)"
replace_env_variables variables.yaml
kubectl apply -f variables.yaml

# Delete previous deployments and services of the same branch, if present
if find_resource deployments "${CI_COMMIT_REG_SLUG}" -q; then
  echo "Erasing previous deployments..."
  kubectl delete deployment "review-$CI_COMMIT_REF_SLUG"
  kubectl delete service "service-$CI_COMMIT_REF_SLUG";
  kubectl get ingress "${CI_PROJECT_NAME}-review" -o yaml | \
    sed '/host: '"$CI_COMMIT_REF_SLUG"'/,+5d' | \
    sed '/-\ '"$CI_COMMIT_REF_SLUG"'/d' > current-ingress.yaml
  sleep 30
fi

# Update current ingress resource if it exists, otherwise create it from zero.
if find_resource ingress "${CI_PROJECT_NAME}"; then
  if [ ! -f current-ingress.yaml ]; then
    echo "Getting current ingress manifest..."
    kubectl get ingress "${CI_PROJECT_NAME}-review" -o yaml > current-ingress.yaml;
  fi
  echo "Updating ingress manifest..."
  sed -n '/spec:/,/tls:/p' current-ingress.yaml | \
    tail -n +3 | \
    head -n -1 >> ingress.yaml
  PREV_HOSTS="$(sed -n '/hosts:/,/secretName:/p' current-ingress.yaml | \
                head -n -1 | \
                tail -n +2)"
  while IFS= read -r LINE; do
    sed -i 's/\ \ \ \ secretName/'"${LINE}"'\n\ \ \ \ secretName/' ingress.yaml;
  done < <(echo "${PREV_HOSTS}")
  kubectl apply -f ingress.yaml;
else
  kubectl apply -f ingress.yaml;
fi

# Deploy pod and service
echo "Deploying latest image..."
kubectl apply -f deploy-integrates.yaml
kubectl rollout status "deploy/review-${CI_COMMIT_REF_SLUG}" --timeout=5m ||
  { echo-blue "Review environment failed to deploy" && exit 1; }

# Erase file with keys
rm variables.yaml
