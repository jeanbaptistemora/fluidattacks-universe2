# shellcheck shell=bash

function main {
  local resolver_test_group="${1}"
  local populate_db="${2:-false}"
  local pytest_args=(
    --cov 'back'
    --cov 'backend'
    --cov-report 'term'
    --cov-report 'annotate:build/functional/annotate'
    --cov-report 'html:build/functional/html'
    --disable-warnings
    --exitfirst
    --no-cov-on-fail
    --resolver-test-group "${resolver_test_group}"
    --verbose
  )

  source __argIntegratesBackEnv__/template dev \
    && DAEMON=true integrates-cache \
    && DAEMON=true integrates-storage \
    && DAEMON=true POPULATE="${populate_db}" integrates-db \
    && echo "[INFO] Running tests for: ${resolver_test_group}" \
    && pushd integrates/back/tests/functional \
    && pytest "${pytest_args[@]}" \
    && popd \
    || return 1
}

main "${@}"
