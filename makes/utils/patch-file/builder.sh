# shellcheck shell=bash

source "${makeSetup}"

function main {
  envsubst \
    -fail-fast \
    -i "${envFile}" \
    -no-empty \
    -no-unset \
    > "${out}"
}


main "${@}"
