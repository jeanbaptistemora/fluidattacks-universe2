# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function main {
  kill_port 4445 \
    && nginx -c __argConfig__/template \
    || return 1
}

main "${@}"
