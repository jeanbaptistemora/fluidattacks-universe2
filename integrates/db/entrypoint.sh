# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

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
    fi \
    || return 1
}

main "${@}"
