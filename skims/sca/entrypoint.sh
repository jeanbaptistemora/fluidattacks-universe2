# shellcheck shell=bash

function main {
  shopt -s nullglob \
    && pushd skims \
    && python3 __argUpdateSCA__ "${@:1}" \
    && popd \
    || return 1

}

main "${@}"
