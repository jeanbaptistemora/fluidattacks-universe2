# shellcheck shell=bash

function main {
  local cluster="common-k8s"
  local region="us-east-1"
  local namespace="dev"
  local regex="integrates-"
  local resources=(
    "deployment"
    "hpa"
    "secret"
    "service"
    "ingress"
  )

  : \
    && aws_login "dev" "3600" \
    && aws_eks_update_kubeconfig "${cluster}" "${region}" \
    && for resource in "${resources[@]}"; do
      kubectl get "${resource}" -n "${namespace}" --no-headers=true 2> /dev/null \
        | awk "/${regex}/{print \$1}" \
        | xargs -r kubectl delete "${resource}" -n "${namespace}"
    done
}

main "${@}"
