# shellcheck shell=bash

function main {
  local resolver_test_group="${1}"
  export COVERAGE_FILE=.coverage."${resolver_test_group}"
  local populate_db="${2:-false}"
  local pytest_args=(
    --cov 'back'
    --cov-report 'term'
    --disable-warnings
    --exitfirst
    --no-cov-on-fail
    --resolver-test-group "${resolver_test_group}"
    --verbose
  )

  sops_export_vars skims/secrets/dev.yaml \
    INTEGRATES_API_TOKEN \
    && DAEMON=true integrates-cache \
    && DAEMON=true integrates-storage \
    && DAEMON=true POPULATE="${populate_db}" dynamodb-for-integrates \
    && echo "[INFO] Running tests for: ${resolver_test_group}" \
    && pushd skims \
    && pytest test/functional/src "${pytest_args[@]}" \
    && popd \
    || return 1
}

main "${@}"
