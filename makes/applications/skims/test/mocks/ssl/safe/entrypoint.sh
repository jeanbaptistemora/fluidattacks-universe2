# shellcheck shell=bash

function main {
  makes-kill-port 4445 \
    && nginx -c __envConfig__ \
    || return 1
}

main "${@}"
