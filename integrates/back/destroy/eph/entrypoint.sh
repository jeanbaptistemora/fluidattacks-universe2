# shellcheck shell=bash

function main {
  local namespace='dev'

  : \
    && aws_login "dev" "3600" \
    && aws_eks_update_kubeconfig common us-east-1 \
    && kubectl delete --all deployment -n "${namespace}" \
    && kubectl delete --all hpa -n "${namespace}" \
    && kubectl delete --all secret -n "${namespace}" \
    && kubectl delete --all service -n "${namespace}" \
    && kubectl delete --all ingress -n "${namespace}"
}

main "${@}"
