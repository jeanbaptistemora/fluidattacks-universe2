# shellcheck shell=bash

function main {
  local pytest_args=(
    --cov 'back'
    --cov 'backend'
    --cov-report 'term'
    --cov-report 'annotate:build/functional/annotate'
    --cov-report 'html:build/functional/html'
    --disable-warnings
    --exitfirst
    --verbose
  )

      source __envIntegratesEnv__ dev \
  &&  DAEMON=true integrates-cache \
  &&  DAEMON=true integrates-db \
  &&  DAEMON=true integrates-storage \
  &&  pushd integrates \
    &&  pytest -m 'priority' "${pytest_args[@]}" test_async/functional_test \
    &&  pytest -m 'not priority' "${pytest_args[@]}" test_async/functional_test \
  &&  popd \
  ||  return 1
}

main "${@}"
