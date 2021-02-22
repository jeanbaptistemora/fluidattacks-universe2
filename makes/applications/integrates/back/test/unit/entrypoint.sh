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
    --ignore 'test_async/functional_test'
    --verbose
  )

      source __envIntegratesEnv__ dev \
  &&  DAEMON=true integrates-cache \
  &&  DAEMON=true integrates-db \
  &&  DAEMON=true integrates-storage \
  &&  pushd integrates \
    &&  pytest -m 'not changes_db' "${pytest_args[@]}" test_async \
    &&  pytest -m 'changes_db' "${pytest_args[@]}" test_async \
  &&  popd \
  ||  return 1
}

main "${@}"
