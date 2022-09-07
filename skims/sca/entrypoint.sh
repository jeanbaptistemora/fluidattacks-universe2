# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function main {
  shopt -s nullglob \
    && pushd skims \
    && python3 __argUpdateSCA__ "${@:1}" \
    && popd \
    || return 1

}

main "${@}"
