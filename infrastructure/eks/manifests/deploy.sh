#!/usr/bin/env bash
set -e

declare -A chart_names_map
declare -A release_names_map
declare -A chart_namespace_map

chart_names_map=( ["nginx"]="stable/nginx-ingress" \
  ["runner"]="gitlab/gitlab-runner" \
  ["cert-manager"]="stable/cert-manager" )
release_names_map=( ["nginx"]="controller" \
  ["runner"]="gitlab-runner" \
  ["cert-manager"]="cert-manager" )
chart_namespace_map=( ["nginx"]="serves"
  ["runner"]="operations"
  ["cert-manager"]="operations" )

function echo-blue() {
  echo -e '\033[1;34m'"${1}"'\033[0m'
}

function get_changed_files() {
  git diff --name-status "${CI_COMMIT_BEFORE_SHA}" "${CI_COMMIT_SHA}" \
    | grep -Po '(?<=(M|A)\t).*'
}

function get_changed_helm_files() {
  mapfile -t changed_files < <(get_changed_files)
  local changed_helm_files=()
  for file in "${changed_files[@]}"; do
    if [[ "${file}" =~ 'helm_values/' ]]; then
      changed_helm_files+=( "${file##*/}" )
    fi
  done
  echo "${changed_helm_files[*]}"
}

function install_helm_chart() {
  local helm_values=( "$@" )
  for file in "${helm_values[@]}"; do
    local file_no_extension="$(echo "${file}" | cut -d. -f1)"
    local chart="${chart_names_map[${file_no_extension}]}"
    local release="${release_names_map[${file_no_extension}]}"
    local namespace="${chart_namespace_map[${file_no_extension}]}"
    if helm list --tls | grep -q "${release}"; then
      echo-blue "Upgrading chart ${chart}..."
      helm upgrade "${release}" "${chart}" -f "${file}" --tls
    else
      echo-blue "Installing chart ${chart}..."
      helm install "${chart}" --name "${release}" -f "${file}" \
        --namespace "${namespace}" --tls
    fi
  done
}

# Set context to avoid using the --namespace flag in every command
kubectl config set-context $(kubectl config current-context) \
  --namespace serves

IFS=" " read -r -a helm_files <<< "$(get_changed_helm_files)"
if [ -z "${helm_files}" ]; then
  echo-blue "Helm values were not updated in this deployment."
else
  helm init --client-only
  helm repo add gitlab https://charts.gitlab.io
  helm repo update
  install_helm_chart "${helm_files[@]}"
fi

# Set TLS certificates for fluidattacks.com and fluid.ls in the NGINX server
sed -i 's/$TLS_KEY/'"$FLUID_TLS_KEY"'/;
  s/$FA_TLS_CERT/'"$FLUIDATTACKS_TLS_CERT"'/;
  s/$FLA_TLS_CERT/'"$FLUIDLA_TLS_CERT"'/' \
  eks/manifests/ingress-tls.yaml
kubectl apply -f eks/manifests/ingress-tls.yaml

# Set Ingress rule and generate certificate for old domains
kubectl apply -f eks/manifests/old-domains.yaml

# Customize NGINX configuration
kubectl patch cm controller-nginx-ingress-controller \
  --patch "$(cat eks/manifests/nginx-conf.yaml)" || \
  echo "NGINX server already configured"

# Provide information to access Gitlab Container Registry and pull images
if ! kubectl get secret gitlab-reg; then
  echo "Creating secret to access Gitlab Registry..."
  kubectl create secret docker-registry gitlab-reg \
    --docker-server="$CI_REGISTRY" --docker-username="$DOCKER_USER" \
    --docker-password="$DOCKER_PASS" --docker-email="$DOCKER_EMAIL"
fi

# Prepare environments for Review Apps
sed 's/$PROJECT/web/g' eks/manifests/review-tmpl.yaml | kubectl apply -f -
sed 's/$PROJECT/integrates/g' eks/manifests/review-tmpl.yaml | kubectl apply -f -

# Install Calico to enforce Network Policies between Pods
# and define policies
kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/release-1.1/config/v1.1/calico.yaml
kubectl apply -f eks/manifests/network-policies.yaml

# Pass variables to Integrates to access Vault
INTEGRATES_VAULT_TOKEN=$(curl --request POST \
  --data '{"role_id":"'"$INTEGRATES_PROD_ROLE_ID"'","secret_id":"'"$INTEGRATES_PROD_SECRET_ID"'"}' \
  "https://$VAULT_S3_BUCKET.com/v1/auth/approle/login" | \
  jq -r '.auth.client_token')
sed -i 's/$VAULT_HOST/'"$(echo -n $VAULT_HOST | base64)"'/;
  s/$VAULT_TOKEN/'"$(echo -n $INTEGRATES_VAULT_TOKEN | base64)"'/' \
        eks/manifests/integrates.yaml

# Deploy apps containers
sed -i 's/$DATE/'"$(date)"'/' eks/manifests/*.yaml
kubectl apply -f eks/manifests/alg.yaml
kubectl rollout status deploy/alg -w

kubectl apply -f eks/manifests/exams.yaml
kubectl rollout status deploy/exams -w

kubectl apply -f eks/manifests/integrates.yaml
kubectl rollout status deploy/integrates -w

kubectl apply -f eks/manifests/vpn.yaml
kubectl rollout status deploy/vpn -w

# Wait until the initialization of the Load Balancer is complete
sleep 5
ELB_NAME="$(aws --region us-east-1 elb describe-load-balancers \
  | jq -r '.LoadBalancerDescriptions[].LoadBalancerName')"
ELB_STATUS="$(aws --region us-east-1 elb describe-instance-health \
  --load-balancer-name $ELB_NAME | jq -r '.InstanceStates[].State')"
I=0
while [[ "$ELB_STATUS" = *"OutOfService"* ]]; do
  echo 'Waiting for Load Balancer to be ready...'
  sleep 10
  ELB_STATUS="$(aws --region us-east-1 elb describe-instance-health \
  --load-balancer-name $ELB_NAME | jq -r '.InstanceStates[].State')"
  I="$((I+1))"
  if [[ "$I" == 10 ]]; then
    echo "Load Balancer failed the Health Checks and is out of service."
    exit 1
  fi
done
echo 'Load Balancer is ready to receive requests.'
