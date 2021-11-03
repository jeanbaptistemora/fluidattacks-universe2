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
  aws_login_dev_new \
    && sops_export_vars __argSecretsFile__ "INTEGRATES_FORCES_API_TOKEN" \
    && integrates-mock '__argDbData__' \
    && pushd forces/ \
    && source __argForcesRuntime__/template \
    && pytest "${args_pytest[@]}" \
    && popd || return 1
}

main "$@"
