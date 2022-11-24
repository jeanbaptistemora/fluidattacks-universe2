# shellcheck shell=bash

function main {
  kill_port 4446 \
    && nginx -c __argConfig__/template \
    || return 1
}

main "${@}"
