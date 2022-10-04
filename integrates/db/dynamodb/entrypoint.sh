# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function main {
  : \
    && data-for-db \
    && dynamodb-for-db \
    || return 1
}

main "${@}"
