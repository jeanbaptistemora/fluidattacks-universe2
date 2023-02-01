# shellcheck shell=bash

function main {
  local namespace="dev"
  local cluster="common-k8s"
  local region="us-east-1"

  : \
    && aws_login "dev" "3600" \
    && aws_eks_update_kubeconfig "${cluster}" "${region}" \
    && kubectl delete --all deployment -n "${namespace}" \
    && kubectl delete --all hpa -n "${namespace}" \
    && kubectl delete --all secret -n "${namespace}" \
    && kubectl delete --all service -n "${namespace}" \
    && kubectl delete --all ingress -n "${namespace}"
}

main "${@}"
