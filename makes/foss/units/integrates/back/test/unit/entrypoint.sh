# shellcheck shell=bash

function main {
  export BATCH_BIN
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

  source __argIntegratesBackEnv__/template dev \
    && DAEMON=true integrates-cache \
    && DAEMON=true integrates-db \
    && DAEMON=true integrates-storage \
    && pushd integrates \
    && BATCH_BIN="$(command -v integrates-batch)" \
    && pytest -m 'not changes_db' "${pytest_args[@]}" back/tests/unit \
    && pytest -m 'changes_db' "${pytest_args[@]}" back/tests/unit \
    && popd \
    || return 1
}

main "${@}"
