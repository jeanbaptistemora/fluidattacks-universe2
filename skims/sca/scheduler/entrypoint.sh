# shellcheck shell=bash

function main {
  local module="${1:-}"

  shopt -s nullglob \
    && if test -z "${module:-}"; then
      echo '[ERROR] Second argument must be the module to execute' \
        && return 1
    fi \
    && aws_login_prod 'skims' \
    && pushd skims \
    && python3 'skims/schedulers/invoker.py' "${module}" \
    && popd \
    || return 1
}

main "${@}"
