# shellcheck shell=bash

function main {
  : \
    && { DAEMON=true dynamodb & } \
    && { DAEMON=true opensearch & } \
    && wait \
    && if [ "${DAEMON:-}" = "true" ]; then
      { integrates-streams dev & }
    else
      integrates-streams dev
    fi

}

main "${@}"
