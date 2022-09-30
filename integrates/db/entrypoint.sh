# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function start_dynamodb {
  : \
    && data-for-db \
    && DAEMON=true dynamodb-for-db \
    || return 1
}

function start_opensearch {
  : \
    && kill_port "9200" \
    && { opensearch & } \
    && wait_port 300 "0.0.0.0:9200" \
    && info "Opensearch is ready" \
    || return 1
}

function start_secondary_datastores {
  : \
    && start_opensearch \
    || return 1
}

function main {
  : \
    && { start_dynamodb & } \
    && { start_secondary_datastores & } \
    && wait \
    && if [ "${DAEMON:-}" = "true" ]; then
      { integrates-streams dev dynamodb & }
    else
      integrates-streams dev dynamodb
    fi \
    || return 1
}

main "${@}"
