# shellcheck shell=bash

function main {
  export API_ENDPOINT="https://localhost:8001/api"

  local args_pytest=(
    --cov-branch
    --cov=forces
    --cov-fail-under '80'
    --cov-report 'term'
    --cov-report "html:${PWD}/integrates/forces/coverage/"
    --cov-report "xml:${PWD}/integrates/forces/coverage.xml"
    --disable-pytest-warnings
    --no-cov-on-fail
    --verbose
  )
  : \
    && aws_login "dev" "3600" \
    && source __argIntegratesBackEnv__/template dev \
    && sops_export_vars __argSecretsFile__ "TEST_FORCES_TOKEN" \
    && DAEMON=true integrates-db \
    && DAEMON=true integrates-back dev \
    && echo "[INFO] Running forces tests..." \
    && pushd integrates/forces/ \
    && source __argForcesRuntime__/template \
    && pytest "${args_pytest[@]}" \
    && popd || return 1
}

main "$@"
