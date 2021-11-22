# shellcheck shell=bash

function main {
  echo '[INFO] Firefox: __argFirefox__' \
    && echo '[INFO] Geckodriver: __argGeckodriver__' \
    && aws_login_dev \
    && sops_export_vars integrates/secrets-development.yaml \
      STARLETTE_SESSION_KEY \
      TEST_E2E_USER_1 \
      TEST_E2E_USER_2 \
      TEST_E2E_USER_3 \
      TEST_E2E_USER_4 \
      TEST_E2E_USER_5 \
    && if test -n "${CI:-}"; then
      aws_eks_update_kubeconfig 'makes-k8s' 'us-east-1' \
        && kubectl rollout status \
          "deploy/integrates-${CI_COMMIT_REF_NAME}" \
          -n "development" \
          --timeout="15m"
    fi \
    && pushd integrates/back/tests/e2e/src \
    && pkgFirefox='__argFirefox__' \
      pkgGeckoDriver='__argGeckodriver__' \
      PYTHONPATH="${PWD}:${PYTHONPATH:-}" \
      pytest "${args_pytest[@]}" \
      --disable-pytest-warnings \
      --exitfirst \
      --reruns 10 \
      --test-group "${CI_NODE_INDEX:-1}" \
      --test-group-count "${CI_NODE_TOTAL:-1}" \
      --verbose \
    && popd \
    || return 1
}

main "${@}"
