# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function main {
  pushd "${envSrc}" \
    && eslint --config .eslintrc . \
    && popd \
    && touch "${out}" \
    || return 1
}

main "${@}"
