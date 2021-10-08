# shellcheck shell=bash

function main {
  export INTEGRATES_FORCES_API_TOKEN
  local args_pytest=(
    --cov-branch
    --cov=forces
    --cov-fail-under '80'
    --cov-report 'term'
    --cov-report "html:${PWD}/forces/coverage/"
    --cov-report "xml:${PWD}/forces/coverage.xml"
    --disable-pytest-warnings
    --no-cov-on-fail
  )

  pushd forces/ \
    && pytest "${args_pytest[@]}" \
    && popd || return 1
}

main "$@"
