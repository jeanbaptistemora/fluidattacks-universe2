# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function main {
  copy "${envSrcIntegratesFront}" "${out}" \
    && copy "${envSetupIntegratesFrontDevRuntime}" "${out}/node_modules" \
    && pushd "${out}" \
    && tcm src/ --silent \
    && tsc -p tsconfig.json \
    && lint_typescript "${out}" "${out}" \
    && popd \
    || return 1
}

main "$@"
