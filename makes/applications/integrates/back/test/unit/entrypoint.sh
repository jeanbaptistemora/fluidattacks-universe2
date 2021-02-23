# shellcheck shell=bash

function main {
  local pytest_args=(
    --cov 'back'
    --cov 'backend'
    --cov-report 'term'
    --cov-report 'html:build/coverage/html'
    --cov-report 'xml:coverage.xml'
    --cov-report 'annotate:build/coverage/annotate'
    --disable-warnings
    --exitfirst
    --verbose
  )

      source __envIntegratesEnv__ dev \
  &&  DAEMON=true integrates-cache \
  &&  DAEMON=true integrates-db \
  &&  DAEMON=true integrates-storage \
  &&  pushd integrates \
    &&  pytest -m 'not changes_db' "${pytest_args[@]}" test_unit \
    &&  pytest -m 'changes_db' "${pytest_args[@]}" test_unit \
  &&  popd \
  ||  return 1
}

main "${@}"
