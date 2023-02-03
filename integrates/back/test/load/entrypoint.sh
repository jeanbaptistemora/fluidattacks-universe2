# shellcheck shell=bash

function main {
  local cluster="common-k8s"
  local region="us-east-1"
  local secrets=(
    TEST_FORCES_TOKEN
  )

  : \
    && pushd integrates/back/test/load \
    && rm -rf node_modules \
    && copy __argRuntime__ node_modules \
    && aws_login "dev" "3600" \
    && sops_export_vars __argSecretsDev__ "${secrets[@]}" \
    && if test -n "${CI:-}"; then
      aws_eks_update_kubeconfig "${cluster}" "${region}" \
        && kubectl rollout status \
          "deploy/integrates-${CI_COMMIT_REF_NAME}" \
          -n "dev" \
          --timeout="15m"
    fi \
    && npm run test \
    && popd \
    || return 1
}

main "${@}"
