# shellcheck shell=bash

function main {
  export INTEGRATES_FORCES_API_TOKEN
  local host="127.0.0.1"
  local port="8022"

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
    && DAEMON=true integrates-back dev \
    && DAEMON=true POPULATE=false integrates-db \
    && DAEMON=true POPULATE=false integrates-storage \
    && DAEMON=true integrates-cache \
    && for data in '__argDbData__/'*'.json'; do
      echo "[INFO] Writing data from: ${data}" \
        && aws dynamodb batch-write-item \
          --endpoint-url "http://${host}:${port}" \
          --request-items "file://${data}" \
        || return 1
    done \
    && pushd forces/ \
    && source __argForcesRuntime__/template \
    && pytest "${args_pytest[@]}" \
    && popd || return 1
}

main "$@"
