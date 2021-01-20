# shellcheck shell=bash

source '__envSetupForcesRuntime__'
source '__envSetupForcesDevelopment__'

function main {
  export INTEGRATES_FORCES_API_TOKEN

  args_pytest=(
    --cov-branch
    --cov-fail-under '80'
    --cov-report 'term'
    --cov-report "html:${PWD}/forces/coverage/"
    --cov-report "xml:${PWD}/forces/coverage.xml"
    --disable-pytest-warnings
  )

      pushd forces/ \
  &&  args_pytest+=( "--cov=forces/" ) \
  &&  pytest "${args_pytest[@]}" \
  &&  popd ||  return 1
}

main "$@"