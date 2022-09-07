# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function main {
  local coverage_args=(
    --omit="back/migrations/*"
    --ignore-errors
  )
  pushd integrates \
    && coverage combine \
    && coverage report "${coverage_args[@]}" \
    && coverage html "${coverage_args[@]}" -d build \
    && coverage xml "${coverage_args[@]}" \
    && mv .coverage .coverage."functional_${1}" \
    && popd \
    || return 1
}

main "${@}"
