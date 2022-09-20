# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# shellcheck shell=bash

function main {
  aws_login "prod_integrates" "3600" \
    && source __argIntegratesBackEnv__/template "prod" \
    && pushd '__argIntegratesSrc__' \
    && celery \
      -A server \
      worker \
      -l INFO \
    && popd || return
}

main "${@}"
