# shellcheck shell=bash

function main {
  local cluster="common-k8s"
  local region="us-east-1"

  : \
    && echo '[INFO] Firefox: __argFirefox__' \
    && echo '[INFO] Geckodriver: __argGeckodriver__' \
    && aws_login "dev" "3600" \
    && sops_export_vars integrates/secrets/development.yaml \
      JWT_ENCRYPTION_KEY \
      JWT_SECRET_HS512 \
      TEST_E2E_USER_1 \
      TEST_E2E_USER_2 \
      TEST_E2E_USER_3 \
      TEST_E2E_USER_4 \
      TEST_E2E_USER_5 \
    && if test -n "${CI:-}"; then
      aws_eks_update_kubeconfig "${cluster}" "${region}" \
        && kubectl rollout status \
          "deploy/integrates-${CI_COMMIT_REF_NAME}" \
          -n "dev" \
          --timeout="15m"
    fi \
    && pushd integrates/back/test/e2e/src \
    && pkgFirefox='__argFirefox__' \
      pkgGeckoDriver='__argGeckodriver__' \
      PYTHONPATH="${PWD}:${PYTHONPATH:-}" \
      pytest "${args_pytest[@]}" \
      --exitfirst \
      --cov . \
      --cov-report 'term' \
      --reruns 10 \
      --test-group "${CI_NODE_INDEX:-1}" \
      --test-group-count "${CI_NODE_TOTAL:-1}" \
      --verbose \
    && popd \
    || return 1
}

main "${@}"
