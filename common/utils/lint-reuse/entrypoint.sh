# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function main {

  pushd __argProjectPath__ \
    && reuse lint \
    && popd \
    || return 1
}

main "${@}"
