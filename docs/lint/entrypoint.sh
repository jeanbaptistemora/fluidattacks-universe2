# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function main {
  : \
    && lint_npm_deps docs/src/package.json \
    || return 1
}

main "${@}"
