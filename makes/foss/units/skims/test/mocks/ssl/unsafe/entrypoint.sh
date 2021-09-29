# shellcheck shell=bash

function main {
  makes-kill-port 4446 \
    && nginx -c __argConfig__/template \
    || return 1
}

main "${@}"
