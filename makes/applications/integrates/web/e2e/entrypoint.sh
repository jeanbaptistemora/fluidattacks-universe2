# shellcheck shell=bash

source '__envSearchPaths__'
source '__envUtilsAws__'
source '__envUtilsSops__'

function main {
      echo '[INFO] Firefox: __envFirefox__' \
  &&  echo '[INFO] Geckodriver: __envGeckodriver__' \
  &&  aws_login_dev integrates \
  &&  sops_export_vars integrates/secrets-development.yaml \
        STARLETTE_SESSION_KEY \
        TEST_E2E_USER \
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
