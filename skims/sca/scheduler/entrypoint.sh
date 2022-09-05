# shellcheck shell=bash

function main {
  local module="${1:-}"

  shopt -s nullglob \
    && if test -z "${module:-}"; then
      echo '[ERROR] Second argument must be the module to execute' \
        && return 1
    fi \
    && aws_login "prod_skims" "3600" \
    && pushd skims \
    && python3 'skims/schedulers/invoker.py' "${module}" \
    && popd \
    || return 1
}

main "${@}"
