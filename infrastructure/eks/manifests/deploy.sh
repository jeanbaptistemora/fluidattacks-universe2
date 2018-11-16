#!/usr/bin/env bash
set -e

function echo-blue() {
  echo -e '\033[1;34m'"${1}"'\033[0m'
}

function replace_env_variables() {
  local files=( "$@" )
  for file in "${files[@]}"; do
    envsubst < "${file}" > tmp
    mv tmp "${file}"
  done
}

function create_kubernetes_namespace() {
  for namespace in "$@"; do
    if kubectl get namespace "${namespace}"; then
      echo-blue "Namespace ${namespace} already exists."
    else
      echo-blue "Creating namespace ${namespace}..."
      kubectl create namespace "${namespace}"
    fi
  done
}

function deploy_application() {
  local manifest="${1}"
  local name="$(echo ${1} | cut -d/ -f2 | cut -d. -f1)"
  replace_env_variables "${manifest}"
  kubectl apply -f "${manifest}"
  kubectl rollout status "deploy/${name}" -w
}

function get_aws_elb_name() {
  aws elb describe-load-balancers | \
    jq -r '.LoadBalancerDescriptions[].LoadBalancerName'
}

function get_aws_elb_status() {
  local name="${1}"
  aws elb describe-instance-health --load-balancer-name "${name}" | \
    jq -r '.InstanceStates[].State'
}

# Get files that were modified or added between the latest commit in master
# and the latest commit in the developer branch
function get_changed_files() {
  git diff --name-status --relative "${CI_COMMIT_BEFORE_SHA}" "${CI_COMMIT_SHA}" \
    | grep -Po '(?<=(M|A)\t).*'
}

function get_vault_approle_token() {
  local role_id="${1}"
  local secret_id="${2}"
  local url="https://${3}/v1/auth/approle/login"
  local data='{"role_id":"'"${role_id}"'","secret_id":"'"${secret_id}"'"}'
  curl --request POST --data "${data}" "${url}" | jq -r '.auth.client_token'
}

function install_helm_chart() {
  local chart="${1}"
  local name="${2}"
  local namespace="${3}"
  local values="helm/${4}"
  if helm list --tls | grep -q "${name}"; then
    mapfile -t changed_files < <(get_changed_files)
    if echo "${changed_files[@]}" | grep -o "${values}"; then
      echo-blue "Upgrading chart ${chart}..."
      helm upgrade "${name}" "${chart}" --values "${values}" --wait --tls
    else
      echo-blue "Chart ${chart} is up to date!"
    fi
  else
    echo-blue "Installing chart ${chart}..."
    helm install "${chart}" --name "${name}" --namespace "${namespace}" \
      --values "${values}" --wait --tls
  fi
}

# Automate the generation and renewal of TLS certificates for secondary domains
function issue_secondary_domain_certificates() {
  local manifest="${1}"
  local secret="${2}"
  local certificate_name="${3}"
  local secret_age="$(kubectl get secret ${secret} | grep -Po '[0-9]+(d|m|s)$' | sed 's/.$//')"
  if [ "${secret_age}" -gt 85 ]; then
    echo-blue "Issuing TLS certificates for secondary domains..."
    kubectl delete secret "${secret}"
    kubectl delete certificate "${certificate_name}"
    kubectl apply -f "${manifest}"
    until kubectl describe certificate "${certificate_name}" | grep 'CertObtained'; do
      echo-blue "Issuing certificate..."
      sleep 10
    done
  else
    echo-blue "Certificates for secondary domains are valid."
  fi
}

function wait_elb_initialization() {
  local elb_name="$(get_aws_elb_name)"
  local elb_status="$(get_aws_elb_status ${elb_name})"
  local i=0
  while [[ "${elb_status}" = *"OutOfService"* ]]; do
    echo-blue 'Waiting for Load Balancer to be ready...'
    sleep 10
    elb_status="$(get_aws_elb_status ${elb_name})"
    i="$((i+1))"
    if [[ "$i" == 10 ]]; then
      echo-blue "Load Balancer failed the Health Checks and is out of service."
      exit 1
    fi
  done
  echo-blue 'Load Balancer is ready to receive requests.'
}


cd eks/manifests/


# Set working namespace to serves to avoid including the flag in every command
create_kubernetes_namespace serves operations integrates web
kubectl config set-context $(kubectl config current-context) \
  --namespace serves


# Set TLS certificates for the main domains and automatically issue valid
# certificates for the secondary domains using Cert-Manager and ACME protocol
replace_env_variables ingress/main-domains.yaml
kubectl apply -f ingress/main-domains.yaml
issue_secondary_domain_certificates ingress/secondary-domains.yaml \
  secondary-domains-cert secondary-domains 


# Provide information to access Gitlab Container Registry and pull images
if ! kubectl get secret gitlab-reg; then
  echo "Creating secret to access Gitlab Registry..."
  kubectl create secret docker-registry gitlab-reg \
    --docker-server="$CI_REGISTRY" --docker-username="$DOCKER_USER" \
    --docker-password="$DOCKER_PASS" --docker-email="$DOCKER_EMAIL"
fi

# Prepare environments for Review Apps
sed 's/$PROJECT/web/g' review-apps/env-template.yaml | kubectl apply -f -
sed 's/$PROJECT/integrates/g' review-apps/env-template.yaml | kubectl apply -f -

# Install Calico to enforce Network Policies between Pods
# and define policies
kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/release-1.1/config/v1.1/calico.yaml
kubectl apply -f review-apps/network-policies.yaml


DATE="$(date)"
FI_VAULT_HOST="$(echo -n ${VAULT_HOST} | base64)"
FI_VAULT_TOKEN="$(get_vault_approle_token ${INTEGRATES_PROD_ROLE_ID} \
  ${INTEGRATES_PROD_SECRET_ID} ${VAULT_HOST} | tr -d '\n' | base64)"
export DATE
export FI_VAULT_HOST
export FI_VAULT_TOKEN

deploy_application deployments/alg.yaml
deploy_application deployments/exams.yaml
deploy_application deployments/integrates.yaml
deploy_application deployments/vpn.yaml


install_helm_chart stable/nginx-ingress controller serves nginx.yaml
install_helm_chart gitlab/gitlab-runner runner operations runner.yaml
install_helm_chart stable/cert-manager cert-manager operations cert-manager.yaml


# Wait until the initialization of the Load Balancer is complete
wait_elb_initialization
