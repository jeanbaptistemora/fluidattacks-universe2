# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function main {

  source __argIntegratesBackEnv__/template dev \
    && pushd integrates \
    && info "Linting schema deprecations..." \
    && python back/lint/schema/deprecations/lint_schema.py \
    && popd \
    || return 1
}

main "${@}"
