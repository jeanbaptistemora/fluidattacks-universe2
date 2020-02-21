#!/usr/bin/env bash
set -e

AMZ_VPC_PLUGIN_VER=1.5.0

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
  local name
  local namespace
  local resource

  name=$(echo "${1}" | cut -d/ -f2 | cut -d. -f1)
  namespace=$(grep -m1 -Po '(?<=namespace: ).*' "${manifest}")
  resource=$(echo "${1}" | cut -d/ -f1)
  replace_env_variables "${manifest}"
  kubectl apply -f "${manifest}"
  kubectl rollout status "${resource}/${name}" -n "${namespace}" --timeout=8m ||
    { kubectl rollout undo "${resource}/${name}" -n "${namespace}" && exit 1; }
}

function find_resource() {
  local resource="${1}"
  local regex="${2}"
  shift 2
  local options="${*}"
  if [ -z "${options}" ]; then
    kubectl get "${resource}" | grep -E "${regex}"
  else
    kubectl get "${resource}" | grep -E "${regex}" "${options}"
  fi
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

function install_helm_chart() {
  local chart="${1}"
  local name="${2}"
  local namespace="${3}"
  local values="helm/${4}"
  local version="${5}"
  replace_env_variables "${values}"
  if helm list --tls | grep -q "${name}"; then
    mapfile -t changed_files < <(get_changed_files)
    if echo "${changed_files[@]}" | grep -o "${values}"; then
      echo-blue "Upgrading chart ${chart}..."
      helm upgrade "${name}" "${chart}" \
        --values "${values}" \
        --version "${version}" \
        --wait \
        --tls
    else
      echo-blue "Chart ${chart} is up to date!"
    fi
  else
    echo-blue "Installing chart ${chart}..."
    helm install "${chart}" \
      --name "${name}" \
      --namespace "${namespace}" \
      --values "${values}" \
      --version "${version}" \
      --wait \
      --tls
  fi
}

function install_amazon_vpc_plugin() {
  local curr_version
  local minor_version

  curr_version="$(kubectl describe daemonset aws-node \
    --namespace kube-system | grep Image | cut -d ':' -f 3)"
  minor_version="v${AMZ_VPC_PLUGIN_VER::-2}"

  if [ "${curr_version}" = "${AMZ_VPC_PLUGIN_VER}" ]; then
    echo-blue "Amazon VPC plugin is up to date"
  else
    kubectl apply -f "vpc-cni-k8s/${minor_version}/aws-k8s-cni.yaml"
    kubectl apply -f "https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/master/config/${minor_version}/calico.yaml"
  fi
}

# Automate the generation and renewal of TLS certificates for secondary domains
function issue_secondary_domain_certificates() {
  local manifest="${1}"
  local tls_manifest
  local secret="${2}"
  local certificate_name="${3}"
  local secret_age

  tls_manifest="$(echo "${manifest}" | cut -d. -f1)-tls.yaml"
  secret_age="$(kubectl get secret "${secret}" | grep -Po '(?<=\s)[0-9]+d' | sed 's/.$//')"
  if [ -z "${secret_age}" ]; then
    echo-blue "Certificates for secondary domains are valid."
  elif [ "${secret_age}" -gt 80 ] || [[ $(get_changed_files) == *"${manifest}"*  ]]; then
    echo-blue "Issuing TLS certificates for secondary domains..."
    kubectl delete "$(echo "${manifest}" | cut -d. -f1)"
    kubectl delete secret "${secret}"
    kubectl delete certificate "${certificate_name}"
    sleep 10
    kubectl apply -f "${tls_manifest}"
    until kubectl describe certificate "${certificate_name}" | grep 'CertObtained'; do
      echo-blue "Issuing certificate..."
      sleep 10
    done
  fi
  kubectl apply -f "${manifest}"
}

function wait_elb_initialization() {
  local elb_name
  local elb_status
  local i=0

  elb_name="$(get_aws_elb_name)"
  elb_status=$(get_aws_elb_status "${elb_name}")

  while [[ "${elb_status}" = *"OutOfService"* ]]; do
    echo-blue 'Waiting for Load Balancer to be ready...'
    sleep 10
    elb_status=$(get_aws_elb_status "${elb_name}")
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
create_kubernetes_namespace serves operations integrates web runners
kubectl config set-context "$(kubectl config current-context)" \
  --namespace serves


helm init --client-only
helm repo add gitlab https://charts.gitlab.io
helm repo add jetstack https://charts.jetstack.io
helm repo add banzaicloud http://kubernetes-charts.banzaicloud.com/branch/master
helm repo update

install_helm_chart stable/nginx-ingress controller serves nginx.yaml 0.24.1
install_helm_chart stable/kube-state-metrics kube-metrics operations metrics.yaml 1.4.0

# Install helm chart for cert-manager, CRDs and labeling is required
kubectl apply -f \
  https://raw.githubusercontent.com/jetstack/cert-manager/release-0.9/deploy/manifests/00-crds.yaml
kubectl label namespace \
  operations certmanager.k8s.io/disable-validation="true" --overwrite
install_helm_chart jetstack/cert-manager cert-manager operations cert-manager.yaml v0.9.1

# Set TLS certificates for the main domains and automatically issue valid
# certificates for the secondary domains using Cert-Manager and ACME protocol
sed -i "s/\$AUTONOMIC_TLS_CERT/$AUTONOMIC_TLS_CERT/g" ingress/autonomic.yaml
sed -i "s/\$AUTONOMIC_TLS_KEY/$AUTONOMIC_TLS_KEY/g" ingress/autonomic.yaml
replace_env_variables ingress/certificates.yaml
kubectl apply -f ingress/certificates.yaml
kubectl apply -f ingress/main-domains.yaml
kubectl apply -f ingress/external.yaml
kubectl apply -f ingress/autonomic.yaml
issue_secondary_domain_certificates ingress/secondary-domains.yaml \
  secondary-domains-cert secondary-domains


# Provide information to access Gitlab Container Registry and pull images
if ! kubectl get secret gitlab-reg; then
  echo "Creating secret to access Gitlab Registry..."
  # Create secret in serves namespace
  kubectl create secret docker-registry gitlab-reg \
    --docker-server="$CI_REGISTRY" --docker-username="$DOCKER_USER" \
    --docker-password="$DOCKER_PASS" --docker-email="$DOCKER_EMAIL" \
  # Copy secret to runners namespace
  kubectl get secret gitlab-reg --export -o yaml | kubectl apply --namespace=runners -f -
fi

# Provide information to access Jfrog Container Registry and pull images
if ! kubectl get secret jfrog-reg --namespace=runners; then
  echo "Creating secret to access JFrog Registry..."
  # Create secret in runners namespace
  kubectl create secret docker-registry jfrog-reg \
    --docker-server="fluid-docker.jfrog.io" --docker-username="$JFROG_USER" \
    --docker-password="$JFROG_PASS" --docker-email="$JFROG_EMAIL" \
    --namespace runners
fi

# Prepare environments for Review Apps
sed 's/$PROJECT/web/g' review-apps/env-template.yaml | kubectl apply -f -
sed 's/$PROJECT/integrates/g' review-apps/env-template.yaml | kubectl apply -f -

# Install Calico to enforce Network Policies between Pods
# and define policies
install_amazon_vpc_plugin
kubectl apply -f review-apps/network-policies.yaml

pushd ../../../
  . ci-scripts/helpers/others.sh
  deploy_integrates
popd

deploy_application deployments/exams.yaml
deploy_application deployments/vpn.yaml
deploy_application daemonsets/newrelic-infra.yaml

# Wait until the initialization of the Load Balancer is complete
wait_elb_initialization
