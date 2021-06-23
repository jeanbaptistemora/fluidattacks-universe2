# shellcheck shell=bash

function main {
  makes-kill-port 4446 \
    && nginx -c __envConfig__ \
    || return 1
}

main "${@}"
