# shellcheck shell=bash

function main {
  local namespace='development'

      aws_login_dev integrates \
  &&  aws_eks_update_kubeconfig integrates-cluster us-east-1 \
  &&  kubectl delete --all deployment -n "${namespace}" \
  &&  kubectl delete --all secret -n "${namespace}" \
  &&  kubectl delete --all service -n "${namespace}" \
  &&  kubectl delete --all ingress -n "${namespace}"
}

main "${@}"
