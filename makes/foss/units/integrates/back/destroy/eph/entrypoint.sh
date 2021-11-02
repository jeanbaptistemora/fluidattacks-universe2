# shellcheck shell=bash

function main {
  local namespace='development'

  aws_login_dev_new \
    && aws_eks_update_kubeconfig makes-k8s us-east-1 \
    && kubectl delete --all deployment -n "${namespace}" \
    && kubectl delete --all hpa -n "${namespace}" \
    && kubectl delete --all secret -n "${namespace}" \
    && kubectl delete --all service -n "${namespace}" \
    && kubectl delete --all ingress -n "${namespace}"
}

main "${@}"
