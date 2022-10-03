# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function main {
  : && pushd integrates/front \
    && copy __argSetupIntegratesFrontDevRuntime__ ./node_modules \
    && tcm src/ --silent \
    && tsc -p tsconfig.json \
    && lint_typescript . . \
    && popd \
    || return 1
}

main "$@"
