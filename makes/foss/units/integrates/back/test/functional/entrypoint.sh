# shellcheck shell=bash

function main {
  export BATCH_BIN
  local resolver_test_group="${1}"
  export COVERAGE_FILE=.coverage."${resolver_test_group}"
  local populate_db="${2:-false}"
  local pytest_args=(
    --cov 'back'
    --cov 'backend'
    --cov-report 'term'
    --cov=myproj
    --disable-warnings
    --exitfirst
    --no-cov-on-fail
    --resolver-test-group "${resolver_test_group}"
    --verbose
  )

  source __argIntegratesBackEnv__/template dev \
    && sops_export_vars integrates/secrets-development.yaml \
      TEST_SSH_KEY \
    && DAEMON=true integrates-cache \
    && DAEMON=true integrates-storage \
    && DAEMON=true POPULATE="${populate_db}" dynamodb-for-integrates \
    && BATCH_BIN="$(command -v integrates-batch)" \
    && echo "[INFO] Running tests for: ${resolver_test_group}" \
    && pushd integrates/back/tests/functional \
    && pytest "${pytest_args[@]}" \
    && popd \
    || return 1
}

main "${@}"
