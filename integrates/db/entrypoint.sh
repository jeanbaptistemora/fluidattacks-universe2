# shellcheck shell=bash

function main {
  : \
    && { DAEMON=true opensearch & } \
    && { DAEMON=true dynamodb & } \
    && wait \
    && if [ "${DAEMON:-}" = "true" ]; then
      { integrates-streams dev & }
    else
      integrates-streams dev
    fi \
    || return 1
}

main "${@}"
