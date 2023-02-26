# shellcheck shell=bash

function main {
  local cluster="common-k8s"
  local region="us-east-1"

  : \
    && if test -n "${CI:-}"; then
      aws_login "dev" "3600" \
        && aws_eks_update_kubeconfig "${cluster}" "${region}" \
        && kubectl rollout status \
          "deploy/integrates-${CI_COMMIT_REF_NAME}" \
          -n "dev" \
          --timeout="15m"
    fi \
    && sops_export_vars __argSecretsDev__ \
      JWT_ENCRYPTION_KEY \
      JWT_SECRET \
      TEST_E2E_USER_1 \
      TESTRIGOR_AUTH_TOKEN \
      TESTRIGOR_SUITE_ID \
    && pushd integrates/web/testrigor \
    && python3 execute.py \
    && popd \
    || return 1
}

main "${@}"
