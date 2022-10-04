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

function main {
  : \
    && { start_dynamodb & } \
    && { DAEMON=true opensearch & } \
    && wait \
    && if [ "${DAEMON:-}" = "true" ]; then
      { integrates-streams dev & }
    else
      integrates-streams dev
    fi \
    || return 1
}

main "${@}"
