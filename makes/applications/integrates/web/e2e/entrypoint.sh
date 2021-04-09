# shellcheck shell=bash

function main {
      echo '[INFO] Firefox: __envFirefox__' \
  &&  echo '[INFO] Geckodriver: __envGeckodriver__' \
  &&  aws_login_dev integrates \
  &&  sops_export_vars integrates/secrets-development.yaml \
        STARLETTE_SESSION_KEY \
        TEST_E2E_USER \
  &&  if test -n "${CI:-}"
      then
            aws_eks_update_kubeconfig 'makes-k8s' 'us-east-1' \
        &&  kubectl rollout status \
              "deploy/integrates-${CI_COMMIT_REF_NAME}" \
              -n "development" \
              --timeout="15m"
      fi \
  &&  pushd integrates/back/tests/e2e/src \
    &&  pkgFirefox='__envFirefox__' \
        pkgGeckoDriver='__envGeckodriver__' \
        PYTHONPATH="${PWD}:${PYTHONPATH:-}" \
        pytest "${args_pytest[@]}" \
          --disable-pytest-warnings \
          --exitfirst \
          --reruns 10 \
          --test-group "${CI_NODE_INDEX:-}" \
          --test-group-count "${CI_NODE_TOTAL:-}" \
          --verbose \
  &&  popd \
  ||  return 1
}

main "${@}"
