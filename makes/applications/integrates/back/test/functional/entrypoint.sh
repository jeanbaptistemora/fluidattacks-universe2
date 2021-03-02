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
  &&  DAEMON=true integrates-storage \
  &&  pushd integrates \
    &&  DAEMON=true POPULATE=true integrates-db \
    &&  pytest -m 'not organizationId' "${pytest_args[@]}" back/tests/functional \
    &&  DAEMON=true POPULATE=false integrates-db \
    &&  pytest -m 'organizationId' "${pytest_args[@]}" back/tests/functional \
  &&  popd \
  ||  return 1
}

main "${@}"
