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
  &&  DAEMON=true PORT=8022 POPULATE=true integrates-db \
  &&  DAEMON=true PORT=8023 POPULATE=false integrates-db \
  &&  DAEMON=true integrates-storage \
  &&  pushd integrates \
    &&  DYNAMODB_PORT=8023 pytest -m 'stateless' "${pytest_args[@]}" test_functional \
    &&  DYNAMODB_PORT=8022 pytest -m 'not stateless' "${pytest_args[@]}" test_functional \
  &&  popd \
  ||  return 1
}

main "${@}"
