# shellcheck shell=bash

function main {
  local env="${1:-}"
  local path="${2:-}"

  source __argIntegratesEnv__ "${env}" \
    && if test "${path}" == ''; then
      echo '[ERROR] Second argument must be the migration file name' \
        && return 1
    fi \
    && pushd integrates/back/migrations \
    && if test "${env}" == 'dev'; then
      python3 "${path}" | tee "${path}.dev.out"
    elif test "${env}" == 'prod'; then
      python3 "${path}"
    else
      echo '[ERROR] First argument must be one of: dev, prod' \
        && return 1
    fi \
    && popd \
    || return 1
}

main "${@}"
