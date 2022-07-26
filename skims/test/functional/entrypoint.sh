# shellcheck shell=bash

function main {
  local skims_test_group="${1}"
  export COVERAGE_FILE=.coverage."${skims_test_group}"
  local populate_db="${2:-false}"
  local pytest_args=(
    --cov 'back'
    --cov-report 'term'
    --disable-warnings
    --exitfirst
    --no-cov-on-fail
    --skims-test-group "${skims_test_group}"
    --verbose
  )

  sops_export_vars skims/secrets/dev.yaml \
    INTEGRATES_API_TOKEN \
    && DAEMON=true integrates-back dev \
    && DAEMON=true integrates-cache \
    && DAEMON=true integrates-storage dev \
    && DAEMON=true POPULATE="${populate_db}" dynamodb-for-integrates \
    && echo "[INFO] Running tests for: ${skims_test_group}" \
    && pushd skims \
    && pytest test/functional/src "${pytest_args[@]}" \
    && popd \
    || return 1
}

main "${@}"
