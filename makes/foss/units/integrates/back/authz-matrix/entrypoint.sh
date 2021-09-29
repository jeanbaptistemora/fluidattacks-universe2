# shellcheck shell=bash

function main {
  local api_status="${1:-no-migration}"

  source __argIntegratesEnv__ dev "${api_status}" \
    && pushd integrates \
    && python3 deploy/permissions_matrix/matrix.py \
    && popd \
    || return 1
}

main "${@}"
