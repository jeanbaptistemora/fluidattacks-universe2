# shellcheck shell=bash

function main {
  export BATCH_BIN
  export COVERAGE_FILE=.coverage.unit
  local pytest_args=(
    --cov 'back'
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
    && DAEMON=true dynamodb-for-integrates \
    && DAEMON=true integrates-storage \
    && pushd integrates \
    && PYTHONPATH="back/src/:back/migrations/:$PYTHONPATH" \
    && BATCH_BIN="$(command -v integrates-batch)" \
    && pytest -m 'not changes_db' "${pytest_args[@]}" back/test/unit/src \
    && pytest -m 'changes_db' "${pytest_args[@]}" back/test/unit/src \
    && popd \
    || return 1
}

main "${@}"
