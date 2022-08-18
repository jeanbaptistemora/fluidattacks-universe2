# shellcheck shell=bash

function main {
  kill_port 4447 \
    && nginx -c __argConfig__/template \
    || return 1
}

main "${@}"
