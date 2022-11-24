# shellcheck shell=bash

function main {
  local action="${1:-}"
  local path="${2:-}"

  shopt -s nullglob \
    && aws_login "prod_skims" "3600" \
    && pushd skims \
    && python3 'skims/sca_patch/__init__.py' "${action}" "${path}" \
    && popd \
    || return 1
}

main "${@}"
