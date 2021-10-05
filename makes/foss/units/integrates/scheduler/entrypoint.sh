# shellcheck shell=bash

function main {
  local env="${1:-}"
  local module="${2:-}"
  local api_status="migration"

  echo "[INFO] Waking up: ${module}" \
    && source __argIntegratesEnv__ "${env}" "${api_status}" \
    && if test -z "${module:-}"; then
      echo '[ERROR] Second argument must be the module to execute' \
        && return 1
    fi \
    && pushd integrates \
    && python3 'back/src/cli/invoker.py' "${module}" \
    && popd \
    || return 1
}

main "${@}"
