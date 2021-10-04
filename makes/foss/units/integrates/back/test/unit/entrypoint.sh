# shellcheck shell=bash

function main {
  local api_status="${1:-no-migration}"
  local pytest_args=(
    --cov 'back'
    --cov 'backend'
    --cov-report 'term'
    --cov-report 'html:build/coverage/html'
    --cov-report 'xml:coverage.xml'
    --cov-report 'annotate:build/coverage/annotate'
    --disable-warnings
    --exitfirst
    --no-cov-on-fail
    --verbose
  )

  source __argIntegratesEnv__ dev "${api_status}" \
    && DAEMON=true integrates-cache \
    && DAEMON=true integrates-db integratesmanager@gmail.com "${api_status}" \
    && DAEMON=true integrates-storage \
    && pushd integrates \
    && export BATCH_BIN='__argBatchBin__' \
    && pytest -m 'not changes_db' "${pytest_args[@]}" back/tests/unit \
    && pytest -m 'changes_db' "${pytest_args[@]}" back/tests/unit \
    && popd \
    || return 1
}

main "${@}"
